# 负责 Meta Brain 的数据访问

from py2neo import Graph, Node, Relationship
from qdrant_client import QdrantClient
from qdrant_client import models as q_models
from rmbcommon.tools import gen_uuid_for_vector
from rmbcommon.models import MetaData, DataSchema, DataTable, DataField
from rmbserver.db_config import meta_graph_db, meta_vector_db
from rmbserver.log import log
from rmbserver import config
from rmbserver.ai import openai_llm


class MetaDAO:
    def __init__(self, graph: Graph, vector: QdrantClient):
        self.graph = graph
        self.vector = vector

    def get_meta_data(self, datasource_id) -> MetaData:
        """
        Get Meta Data from MetaBrain
        """
        # Find the DataSource node
        datasource_node = self.graph.nodes.match("sources", id=datasource_id).first()
        if not datasource_node:
            raise ValueError(f"DataSource with id {datasource_id} not found")
        datasource_name = datasource_node['name']
        metadata = MetaData(datasource_name, datasource_id=datasource_id)

        # 查询与特定数据源相关的所有schema
        schemas = self.graph.run("MATCH (d:sources)-[:D2S]->(s:schemas) "
                                 "WHERE d.id = $datasource_id RETURN s",
                                 datasource_id=datasource_id).data()
        # log.debug(f"从 MetaBrain 查询到的 schema: {[s['s']['name'] for s in schemas]}")
        for schema_data in schemas:
            schema_name = schema_data['s']['name']
            schema = DataSchema(metadata=metadata, **schema_data['s'])

            # 查询与特定模式相关的所有表
            tables = self.graph.run(
                "MATCH (d:sources)-[:D2S]->(s:schemas)-[:S2T]->(t:tables) "
                "WHERE d.id = $datasource_id AND s.name = $schema_name RETURN t",
                datasource_id=datasource_id, schema_name=schema_name).data()
            # log.debug(f"从 MetaBrain 查询到的 table: {[t['t']['name'] for t in tables]}")
            for table_data in tables:
                table_name = table_data['t']['name']
                table = DataTable(schema=schema, **table_data['t'])
                fields = self.graph.run(
                    "MATCH (d:sources)-[:D2S]->(s:schemas)-[:S2T]->(t:tables)-[:T2F]->(f:fields) "
                    "WHERE d.id = $datasource_id AND s.name = $schema_name "
                    "and t.name = $table_name RETURN f",
                    datasource_id=datasource_id,
                    schema_name=schema_name,
                    table_name=table_name
                ).data()
                # log.debug(f"从 MetaBrain 查询到的 field: {[f['f']['name'] for f in fields]}")
                for field_data in fields:
                    field = DataField(table=table, **field_data['f'])
                    table.add_field(field)

                schema.add_table(table)

            metadata.add_schema(schema)

        # 处理字段之间的 F2F 关系
        field_relations = self.graph.run("MATCH (f1:fields)-[:F2F]->(f2:fields) RETURN f1, f2").data()
        # log.debug(f"从 MetaBrain 查询到的 field 关联关系: "
        #           f"{[(r['f1']['name'], r['f2']['name']) for r in field_relations]}")
        for relation in field_relations:
            source_full_name = f"{relation['f1']['full_name']}"
            target_full_name = f"{relation['f2']['full_name']}"

            source_field = metadata.get_field_by_full_name(source_full_name)
            target_field = metadata.get_field_by_full_name(target_full_name)

            if source_field and target_field:
                target_field.set_related_field(source_field)
                # source_field.set_related_field(target_field)
        # log.debug(metadata.to_string())
        return metadata

    def sync_to_vector(self, datasource_id, metadata: MetaData):
        collection_name = datasource_id

        # 重建新的集合，每次都情况重写，简单点 TODO：可优化
        self.vector.recreate_collection(
            collection_name=collection_name,
            vectors_config=q_models.VectorParams(
                size=config.openai_embedding_vector_size,
                distance=q_models.Distance.COSINE
            ),
        )

        # 准备要插入的数据点
        points = []
        entities = []

        for schema in metadata.schemas:
            entities.append(("schema", schema.name, schema.curr_desc))
            # log.debug(f"更新Vector数据： schema= {schema.name}, "
            #           f"{schema.curr_desc}, {[t.name for t in schema.tables]}")
            for table in schema.tables:
                entities.append(("table", table.full_name, table.curr_desc))
                # log.debug(f"更新 Vector 数据：table={table.name}, "
                #           f"{table.curr_desc}, {[f.curr_desc for f in table.fields]}")
                for field in table.fields:
                    entities.append(("field", field.full_name, field.curr_desc))

        # 按照批处理生成嵌入
        _BATCH_SIZE = 100
        for i in range(0, len(entities), _BATCH_SIZE):
            batch_texts = [entity[2] or '' for entity in entities[i:i + _BATCH_SIZE]]
            _embeddings = openai_llm.embedding_batch(batch_texts)
            for j, (entity_type, entity_name, entity_desc) in enumerate(entities[i:i + _BATCH_SIZE]):
                points.append(
                    q_models.PointStruct(
                        id=gen_uuid_for_vector(),
                        vector=_embeddings[j],
                        payload={"type": entity_type, "name": entity_name, "desc": entity_desc}
                    )
                )

        # 插入数据点
        self.vector.upsert(collection_name=collection_name, points=points)
        log.debug(f"插入了 {len(points)} 个向量。")
        return len(points)

    def find_meta_data_by_question(self, question: str,
                                   datasource_id: str,
                                   search_limit: int = 100,
                                   top_n: int = 10,
                                   table_score_threshold: float = 4.0
                                   ) -> MetaData:
        # TODO:重新检查一遍，有bug，还没用上
        # Step 1: Create the embedding for the question using openai_llm
        question_embedding = openai_llm.embedding(question)

        # Search the vector database
        collection_name = datasource_id
        results = self.vector.search(
            collection_name=collection_name,
            query_vector=question_embedding,
            limit=search_limit
        )

        # Initialize MetaData
        metadata = MetaData(name="SearchResults")

        # Process search results
        for result in results:
            entity_type = result.payload["type"]
            entity_name = result.payload["name"]
            entity_desc = result.payload["desc"]

            # Depending on the entity type, we add it to the metadata
            if entity_type == "schema":
                metadata.add_schema(DataSchema(name=entity_name, metadata=metadata, origin_desc=entity_desc))
            elif entity_type == "table":
                # Extract schema name and table name
                schema_name, table_name = entity_name.split('.')
                schema = metadata.get_schema_by_name(schema_name)
                if schema:
                    schema.add_table(DataTable(name=table_name, schema=schema, origin_desc=entity_desc))
            elif entity_type == "field":
                # Extract schema name, table name, and field name
                schema_name, table_name, field_name = entity_name.split('.')
                schema = metadata.get_schema_by_name(schema_name)
                if schema:
                    table = schema.get_table_by_name(table_name)
                    if table:
                        table.add_field(DataField(name=field_name, table=table, origin_desc=entity_desc))

        # Return the metadata
        return metadata

    def _update_exists_object_desc(self, node, origin_desc):
        """ Update Description
            3.1 如果metadata中存在origin_desc，则直接更新图中的 origin_desc
            3.2 如果图中的curr_desc 为空：直接使用新的 origin_desc 作为 curr_desc
            3.3 如果图中的curr_desc 不为空：
                    如果curr_desc 没有被人为设置过的话（curr_desc_stat!='human'），
                    直接使用新的 origin_desc 作为 curr_desc。
        """
        if origin_desc:
            # log.debug(f"更新描述: origin_desc={origin_desc}")
            node['origin_desc'] = origin_desc
            if not node['curr_desc']:
                # log.debug(f"curr_desc 没有内容，直接更新描述: curr_desc={origin_desc}")
                node['curr_desc'] = origin_desc
                node['curr_desc_stat'] = 'origin'
            elif node['curr_desc_stat'] in ('origin', 'ai'):  # not config by human
                # log.debug(f"curr_desc 有内容，但没有被人为设置过，继续更新描述: curr_desc={origin_desc}")
                node['curr_desc'] = origin_desc
                node['curr_desc_stat'] = 'origin'
        return node

    def sync_to_graph(self, datasource_id, meta_data: MetaData):
        """
        Save or Update Meta Data
        1，保存 MetaData 中的所有 DataSchema、DataTable、DataField
        2，删除不再存在的 DataSchema、DataTable、DataField
        3，更新 MetaData 中的所有 DataSchema、DataTable、DataField（描述）
        """
        # 找到 DataSource 节点
        datasource_node = self.graph.nodes.match("sources", id=datasource_id).first()
        if not datasource_node:
            raise ValueError(f"DataSource with id {datasource_id} not found")

        tx = self.graph.begin()

        # 获取与 DataSource 直接关联的所有 DataSchema 节点
        schema_nodes = self.graph.match(nodes=(datasource_node, None), r_type="D2S")
        existing_schemas = {node.end_node['name']: node.end_node for node in schema_nodes}
        # log.debug(f"MetaBrain 中所有的 schema：{existing_schemas.keys()}")

        # 遍历 MetaData 中的所有 DataSchema
        # log.debug(f"开始遍历 Runtime 中的 schema: {[s.name for s in meta_data.schemas]}")
        for schema in meta_data.schemas:
            schema_node = existing_schemas.pop(schema.name, None)

            if not schema_node:
                # 创建 DataSchema 节点
                # log.debug(f"schema {schema.name}不存在，创建新的schema节点")
                schema_node = Node("schemas", **schema.db_properties)
                self.graph.create(schema_node)

                # 关联 DataSource 和 DataSchema
                # log.debug(f"创建 schema 节点成功，创建schema和datasource的关系: {datasource_id} -> {schema.name}")
                self.graph.create(Relationship(datasource_node, "D2S", schema_node))
            else:
                # 更新 DataSchema 节点
                schema_node = self._update_exists_object_desc(schema_node, schema.origin_desc)
                self.graph.push(schema_node)

            # 获取与当前 DataSchema 关联的所有 DataTable 节点
            table_nodes = self.graph.match(nodes=(schema_node, None), r_type="S2T")
            existing_tables = {node.end_node['name']: node.end_node for node in table_nodes}
            # log.debug(f"获取 MetaBrain 中 schema {schema.name}下的所有table: {existing_tables.keys()}")

            # 遍历 DataSchema 中的所有 DataTable
            # log.debug(f"开始遍历 Runtime 中的schema {schema.name}下的所有table: {[t.name for t in schema.tables]}")
            for table in schema.tables:
                table_node = existing_tables.pop(table.name, None)

                if not table_node:
                    # 创建 DataTable 节点
                    # log.debug(f"table {table.name}不存在，创建新的 table 节点: {table.db_properties}")
                    table_node = Node("tables", **table.db_properties)
                    self.graph.create(table_node)

                    # 关联 DataSchema 和 DataTable
                    # log.debug(f"创建 table节点成功，创建table和schema的关系: {schema.name} -> {table.name}")
                    self.graph.create(Relationship(schema_node, "S2T", table_node))
                else:
                    # 更新 DataTable 节点
                    table_node = self._update_exists_object_desc(table_node, table.origin_desc)
                    self.graph.push(table_node)

                # 获取与当前 DataTable 关联的所有 DataField 节点
                field_nodes = self.graph.match(nodes=(table_node, None), r_type="T2F")
                existing_fields = {node.end_node['name']: node.end_node for node in field_nodes}
                # log.debug(f"获取 MetaBrain 中 table {table.name}下的所有field: {existing_fields.keys()}")

                # 遍历 DataTable 中的所有 DataField
                # log.debug(f"开始遍历 Runtime 中的table {table.name}下的所有field: {[f.name for f in table.fields]}")
                for field in table.fields:
                    field_node = existing_fields.pop(field.name, None)

                    if not field_node:
                        # 创建 DataField 节点
                        # log.debug(f"field {field.name}不存在，创建新的field节点: {field.db_properties}")
                        field_node = Node("fields", **field.db_properties)
                        self.graph.create(field_node)

                        # 关联 DataTable 和 DataField
                        # log.debug(f"创建field节点成功，创建field和table的关系: {table.name} -> {field.name}")
                        self.graph.create(Relationship(table_node, "T2F", field_node))
                    else:
                        # 更新 DataField 节点
                        field_node = self._update_exists_object_desc(field_node, field.origin_desc)
                        self.graph.push(field_node)

                # 删除不再存在的 DataField
                if existing_fields:
                    for field_node in existing_fields.values():
                        log.info(f"清理 MetaBrain 中的废弃字段：{table.name}.{field_node['name']}")
                        self.graph.delete(field_node)
                else:
                    # log.info(f"MetaBrain 的表{table.name} 没有废弃字段")
                    pass

            # 删除不再存在的 DataTable
            if existing_tables:
                delete_query = """
                    MATCH (d:sources)-[:D2S]->(s:schemas)-[:S2T]->(t:tables)-[:T2F]->(f:fields)
                    WHERE d.id = $datasource_id AND s.name = $schema_name AND t.name IN $table_names
                    DETACH DELETE t, f
                """
                log.info(f"清理 MetaBrain 中的废弃表: {existing_tables.keys()}")
                self.graph.run(delete_query, datasource_id=datasource_id, schema_name=schema.name,
                               table_names=[t for t in existing_tables.keys()])
            else:
                # log.info(f"MetaBrain 的 {schema.name} 下没有废弃表")
                pass

        # 删除不再存在的 DataSchema
        if existing_schemas:
            delete_query = """
                MATCH (d:sources)-[:D2S]->(s:schemas)-[:S2T]->(t:tables)-[:T2F]->(f:fields)
                WHERE d.id = $datasource_id AND s.name IN $schema_names
                DETACH DELETE s, t, f
            """
            log.info(f"清理 MetaBrain 中的废弃 schema: {existing_schemas.keys()}")
            self.graph.run(delete_query, datasource_id=datasource_id,
                           schema_names=[s for s in existing_schemas.keys()])
        else:
            # log.info(f"MetaBrain 中没有废弃的 schema")
            pass

        # 确保一次性提交所有更改
        self.graph.commit(tx)

    def update_meta_data_in_graph(self, datasource_id, meta_data: MetaData):
        """ Update Meta Data in Graph
        只更新 MetaBrain 中的Graph，不增加，也不删除，主要是为了更新描述
        # TODO 更新relations
        """
        # 更新 schema 的 curr_desc
        for schema in meta_data.schemas:
            #
            self.graph.run(
                """
                MATCH (d:sources {id: $datasource_id})-[:D2S]->(s:schemas {name: $schema_name})
                SET s.curr_desc = $curr_desc, s.curr_desc_stat = 'ai'
                """,
                datasource_id=datasource_id,
                schema_name=schema.name,
                curr_desc=schema.curr_desc
            )

            # 更新 schema 下的每个 table 的 curr_desc
            for table in schema.tables:
                self.graph.run(
                    """
                    MATCH (d:sources {id: $datasource_id})-[:D2S]->(s:schemas)-
                    [:S2T]->(t:tables {name: $table_name})
                    SET t.curr_desc = $curr_desc, t.curr_desc_stat = 'ai'
                    """,
                    datasource_id=datasource_id,
                    table_name=table.name,
                    curr_desc=table.curr_desc
                )

                # 更新 table 下的每个 field 的 curr_desc
                for field in table.fields:
                    self.graph.run(
                        """
                        MATCH (d:sources {id: $datasource_id})-[:D2S]->(s:schemas)-
                        [:S2T]->(t:tables)-[:T2F]->(f:fields {name: $field_name})
                        SET f.curr_desc = $curr_desc, f.curr_desc_stat = 'ai'
                        """,
                        datasource_id=datasource_id,
                        field_name=field.name,
                        curr_desc=field.curr_desc,
                    )

    def delete_meta_data_from_graph(self, datasource_id):
        """
        delete meta from brain
        """
        # 构建并执行级联删除的 Cypher 查询
        query = """
        MATCH (ds:sources {id: $datasource_id})
        OPTIONAL MATCH (ds)-[:D2S]->(schema)
        OPTIONAL MATCH (schema)-[:S2T]->(table)
        OPTIONAL MATCH (table)-[:T2F]->(field)
        OPTIONAL MATCH (field)-[:F2F]->(related_field)
        DETACH DELETE schema, table, field, related_field
        """
        self.graph.run(query, datasource_id=datasource_id)

    def delete_meta_data_from_vector(self, datasource_id):
        # 删除向量
        self.vector.delete_collection(collection_name=datasource_id)

    def only_for_test_clear_all(self):
        self.graph.delete_all()
        for collection in self.vector.get_collections().collections:
            self.vector.delete_collection(collection_name=collection.name)
        log.info(f"All Brain Meta cleared!")


meta_dao = MetaDAO(meta_graph_db, meta_vector_db)
