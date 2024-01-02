# IDC 中对数据源的操作，都是通过 DataSourceManager 来完成的，是RMB(MetaBrain)的中枢
# 比如：访问数据源，推理 MetaData，保存到 MetaBrain

# from rmbcommon.models import MetaData
# from rmbserver.log import log
# from rmbserver.ai.tools.meta import gen_meta_desc_and_relations
# from rmbserver.exceptions import DataSourceNotFound
# from rmbserver.brain.dao_meta import meta_dao
# from rmbserver.brain.dao_service import service_dao
from rmbserver.brain.datasource import DataSource

class DataSourceManager:

    def __init__(self, datasource_id: str):
        self.data_source = DataSource.get(datasource_id)

    @staticmethod
    def get_all_datasources(name=None):
        return DataSource.list(name)

    @staticmethod
    def create_datasource(ds_name, ds_type, ds_access_config):
        """
        创建数据源
        """
        return DataSource.create(ds_name, ds_type, ds_access_config)


