from rmbclient.rmb import ReliableMetaBrain as RMB
from rmbclient.api import ResourceNotFound
from unittest import TestCase
from rmbclient.log import log


class TestMeta(TestCase):
    # 初始化 Meta Brain 实例
    data = RMB(token="token3", debug=True)  # 使用有效的测试Token

    def _create(self):
        # 注册数据源
        ds = self.data.datasources.register(
            ds_type="MySQL", ds_name="我的MySQL库",
            # ds_access_config={
            #     "host": "fbi.chat",
            #     "port": 3306,
            #     "user": "root",
            #     "password": "Pass1234"
            # })
            ds_access_config={
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": ""
            })
        return ds

    def _get_or_create_ds(self):
        name = "我的MySQL库"
        try:
            ds = self.data.datasources.get(name=name)
            log.info(f"datasource {name} found")
        except ResourceNotFound:
            ds = self._create()
            log.info(f"datasource {name} created")
        return ds

    def test_sync_meta(self):
        # 获取数据源
        ds = self._get_or_create_ds()
        runtime_meta = ds.meta.get('runtime')
        print(runtime_meta.to_string())

        ds_copy = self.data.datasources.get(id=ds.id)
        ds_copy_id = ds_copy.id
        ds_list = self.data.datasources
        log.info(f"metadata in runtime: {ds.meta.get('runtime').to_dict()}")
        log.info(f"metadata in brain: {ds.meta.get('in_brain')}")
        ds.meta.sync()
        log.info(f"metadata in brain: {ds.meta.get('in_brain').to_string()}")
        schema_list = ds.meta.get('in_brain').schemas
        log.info(f"schemas: {schema_list}")
        # ds.delete()
