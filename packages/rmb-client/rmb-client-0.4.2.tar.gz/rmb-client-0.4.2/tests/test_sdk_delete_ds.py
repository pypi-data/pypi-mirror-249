from rmbclient.resources import ReliableMetaBrain as RMB
from unittest import TestCase
from rmbclient.log import log

class TestDataResource(TestCase):
    def test_clear(self):

        # 初始化 IntelligentDataCortex 实例
        data = RMB(token="token1", debug=True)
        for ds in data.datasources:
            log.debug(f"删除数据源:  {ds}")
            ds.delete()

        data.test_clear_all()
