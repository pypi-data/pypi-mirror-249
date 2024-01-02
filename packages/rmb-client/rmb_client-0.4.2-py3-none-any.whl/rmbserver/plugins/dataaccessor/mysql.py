import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
import pandas as pd
from rmbserver.plugins.dataaccessor.da_base import BaseDataAccessor
from rmbserver.plugins.dataaccessor.da_register import register_data_accessor
from rmbserver.log import log
from rmbserver.plugins.model.mysql import MySQLQuery, MySQLQueryResult
from rmbcommon.models import MetaData, DataSchema, DataTable, DataField


@register_data_accessor
class MySQLDataAccessor(BaseDataAccessor):
    # 从 BaseDataAccessor 继承，创建一个新的数据源类
    # 必须要指定 __source_type__，与添加的Type保持一致，这样才能找到对应的数据源类
    __source_type__ = "MySQL"
    __access_config_keys_must__ = ['user', 'password', 'host']
    __access_config_keys_safe__ = ['host', 'port', 'user']

    __ignore_schemas__ = ['information_schema',
                          'mysql',
                          'performance_schema',
                          'sys',
                          'datamini_openai',
                          'cmysql_test',
                          'datamini_openai_test'
                          ]

    PROMPT_GEN_STRUC_QUERY = """
    这是一个 MySQL 数据库。请根据要求提供可以直接执行的SQL语句，SQL语句中包含schema名称，避免歧义。
    """

    def _get_db_engine(self):
        # 构建数据库连接URL
        self.ds_port = self.ds_access_config.get('port', 3306)
        self.database_url = (f"mysql+pymysql://{self.ds_user}:"
                             f"{self.ds_password}@{self.ds_host}:{self.ds_port}/")

        # 创建SQLAlchemy引擎
        return create_engine(self.database_url)

    def retrieve_meta_data(self) -> MetaData:
        # 获取DB Engine
        engine = self._get_db_engine()

        # New MetaData
        metadata_object = MetaData(name=f"MySQL_{self.ds_host}:{self.ds_port}")

        try:
            # 连接数据库
            with engine.connect() as conn:
                # 使用Inspector获取数据库信息
                inspector = sqlalchemy.inspect(engine)

                # 获取所有的数据库（schema）
                schemas = inspector.get_schema_names()
                for schema in schemas:
                    # 忽略系统数据库
                    if schema in self.__ignore_schemas__:
                        continue

                    # 如果在access_config中指定了db，则只访问这个db的数据
                    access_db = self.ds_access_config.get('db', None)
                    if access_db:
                        if schema != access_db:
                            continue

                    # 创建一个DataSchema对象
                    data_schema = DataSchema(
                        name=schema,
                        metadata=metadata_object,
                        origin_desc=""
                    )

                    # 获取当前schema中的所有表
                    tables = inspector.get_table_names(schema=schema)
                    for table_name in tables:
                        # 获取表的备注信息
                        table_comment = inspector.get_table_comment(
                            table_name,
                            schema=schema
                        )['text']

                        # 创建DataTable对象
                        data_table = DataTable(
                            name=table_name,
                            origin_desc=table_comment if table_comment else "",
                            schema=data_schema
                        )

                        # 获取表的列
                        columns = inspector.get_columns(table_name, schema=schema)
                        for column in columns:
                            # 创建DataField对象
                            data_field = DataField(
                                name=column['name'],
                                origin_desc=column.get('comment', ''),
                                table=data_table
                            )

                            data_table.add_field(data_field)

                        # 将DataTable添加到DataSchema
                        data_schema.add_table(data_table)

                    # 将DataSchema添加到MetaData
                    metadata_object.add_schema(data_schema)

        except SQLAlchemyError as e:
            log.error(f"An error occurred: {e}")
        finally:
            engine.dispose()

        return metadata_object

    def query(self, struc_query: MySQLQuery, meta_data: MetaData) -> MySQLQueryResult:
        sql = struc_query.content
        log.debug(f"执行SQL语句：{sql}")

        if not isinstance(sql, str):
            raise TypeError(f"sql must be a string, not {type(sql)}")

        engine = self._get_db_engine()
        with engine.connect() as conn, conn.begin():
            df = pd.read_sql(sql, conn)

        return MySQLQueryResult(query=struc_query, result=df)


log.info(f"registering data accessor: {MySQLDataAccessor.__source_type__}")
