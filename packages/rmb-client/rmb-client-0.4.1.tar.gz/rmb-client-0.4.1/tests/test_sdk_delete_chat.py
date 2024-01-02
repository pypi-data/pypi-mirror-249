from rmbclient import RMB
from unittest import TestCase

class TestDataResource(TestCase):
    def test_clear(self):

        # 初始化 IntelligentDataCortex 实例
        data = RMB(token="token1", debug=True)
        data.test_clear_chat()
