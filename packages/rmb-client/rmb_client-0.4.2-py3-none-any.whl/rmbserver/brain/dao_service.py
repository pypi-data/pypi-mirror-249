
import json
from py2neo import NodeMatcher, Graph, Node

from rmbserver.log import log
from rmbserver.db_config import service_graph_db
from rmbserver.exceptions import DataSourceExists
from rmbcommon.tools import gen_id_for_graph
from rmbcommon.models import DataSourceCore


class RMBServiceDAO(object):
    """ Data Access Object for RMB
    """

    def __init__(self, graph: Graph):
        self.graph = graph
        # 创建一个 NodeMatcher 实例
        self.matcher = NodeMatcher(self.graph)

    def _dump_node(self, node: Node) -> dict or None:
        if not node:
            return None
        return {
            'id': node['id'],
            'name': node['name'],
            'type': node['type'],
            'access_config': json.loads(node['access_config']),
        }

    def get_all_datasources(self) -> list[DataSourceCore]:
        """ Get all datasources
        """
        ds_node_list = self.matcher.match("sources")
        return [DataSourceCore.load_from_dict(self._dump_node(ds_node))
                for ds_node in ds_node_list]

    def get_ds_node_by_id(self, ds_id) -> Node or None:
        """ Get a datasource node by id
        """
        return self.matcher.match("sources", id=ds_id).first()

    def get_datasource_by_id(self, ds_id) -> DataSourceCore or None:
        """ Get a datasource by id
        """
        # 执行查询，根据 ID 查询 DataSource 节点
        ds_node = self.get_ds_node_by_id(ds_id)
        return DataSourceCore.load_from_dict(self._dump_node(ds_node))

    def get_datasource_by_name(self, ds_name) -> DataSourceCore or None:
        """ Get a datasource by name
        """
        ds_node = self.matcher.match("sources", name=ds_name).first()
        return DataSourceCore.load_from_dict(self._dump_node(ds_node))

    def get_datasource_by_access_config(
            self, ds_access_config: dict
    ) -> DataSourceCore or None:
        """ Get a datasource by access config
        """
        ds_node = self.matcher.match(
            "DataSource",
            access_config=json.dumps(ds_access_config)
        ).first()
        return DataSourceCore.load_from_dict(self._dump_node(ds_node))

    def add_datasource(
            self, ds_name, ds_type, ds_access_config: dict
    ) -> DataSourceCore:
        """ Add a datasource
        """
        if self.get_datasource_by_access_config(ds_access_config):
            log.warning(f"DataSource access config already exists")
            raise DataSourceExists(f"DataSource access config already exists")

        if self.get_datasource_by_name(ds_name):
            log.warning(f"DataSource {ds_name} already exists")
            raise DataSourceExists(f"DataSource {ds_name} already exists")

        datasource_node = Node(
            "sources",
            id=gen_id_for_graph(), name=ds_name, type=ds_type,
            access_config=json.dumps(ds_access_config)
        )
        self.graph.create(datasource_node)
        return DataSourceCore.load_from_dict(self._dump_node(datasource_node))

    def delete_datasource(self, datasource_id):
        """ Delete a datasource
        """
        ds_node = self.get_ds_node_by_id(datasource_id)
        if ds_node:
            self.graph.delete(ds_node)
            return True
        else:
            log.error(f"DataSource with id {datasource_id} not found")
            return False

    def check_datasource_ids(self, datasource_ids: list[str]) -> list:
        """ Check if datasource ids are valid
        """
        invalid_datasource_ids = []
        for ds_id in datasource_ids:
            if not self.get_ds_node_by_id(ds_id):
                invalid_datasource_ids.append(ds_id)
        return invalid_datasource_ids


service_dao = RMBServiceDAO(service_graph_db)
