from rmbclient.rmb import ReliableMetaBrain as RMB
import unittest
from rmbclient.log import log


class TestChat(unittest.TestCase):
    data = RMB(token="token3", debug=True)

    def test_chat(self):
        datasource_ids = [ds.id for ds in self.data.datasources]

        # 注册数据源
        chat = self.data.chats.create(datasource_ids)
        log.info(f"获取刚刚创建的对话: {self.data.chats.get(chat.id)}")

        log.info(f"获取所有对话: {self.data.chats.to_dict()}")

        # 查询对话

        log.info(f"向 {chat} 中发送消息1: {chat.messages.create('你好')}")
        log.info(f"向 {chat} 中发送消息2: {chat.messages.create('我是张三')}")
        log.info(f"{chat} 中的所有消息: {chat.messages.to_dict()}")

        log.info(f"{chat} 开始运行AI回复消息...")
        run = chat.runs.create()
        log.debug(f"{chat} 运行完成")
        log.info(f"查看AI运行状态 {chat}: {chat.runs.get(run.id)}")

        chat.ask('我是张三吗？')
        chat.ask('我叫什么')
        assert len(chat.messages.to_dict()) == 6

        # 删除对话
        chat.delete()

