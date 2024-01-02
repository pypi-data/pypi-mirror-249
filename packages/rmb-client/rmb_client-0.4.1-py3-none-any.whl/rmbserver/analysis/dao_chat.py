from rmbserver import config
import time
from rmbserver.log import log
from rmbserver.db_config import chat_mongodb
from rmbcommon.tools import gen_id_for_chat, gen_id_for_msg, gen_id_for_run
from rmbcommon.models import ChatCore, MessageCore, RunCore


class ChatDAO:
    def __init__(self, mongodb_client, dbname):
        self.client = mongodb_client
        self.db = self.client[dbname]
        self.chats = self.db.chats

    def _change_id(self, mongo_dict) -> dict or None:
        if not mongo_dict:
            return None
        mongo_dict['id'] = mongo_dict.pop('_id')
        return mongo_dict

    def create_chat(self, datasource_ids: list[str]) -> ChatCore:
        chat_id = gen_id_for_chat()
        chat = {
            '_id': chat_id,
            'datasource_ids': datasource_ids,
            'created': int(time.time()),
            'messages': []
        }
        self.chats.insert_one(chat)
        return ChatCore.load_from_dict(self._change_id(chat))

    def get_chats(self, limit=100, order_by='created') -> list[ChatCore]:
        # 不包含历史消息
        chats = self.chats.find({}, {'messages': 0}).sort(order_by, -1).limit(limit)
        return [ChatCore.load_from_dict(self._change_id(chat)) for chat in chats]

    def add_message(self, chat_id, role, content) -> MessageCore:
        msg_id = gen_id_for_msg()
        msg = {
            'id': msg_id,
            'created': int(time.time()),
            'role': role,
            'content': content,
        }
        # 更新聊天记录，添加新的消息
        result = self.chats.update_one({'_id': chat_id}, {'$push': {'messages': msg}})
        msg['chat_id'] = chat_id
        return MessageCore.load_from_dict(msg)

    def get_chat(self, chat_id) -> ChatCore:
        # 修改 projection 排除 messages 和 runs 字段
        projection = {'messages': 0, 'runs': 0}

        # 执行查询
        chat = self.chats.find_one({'_id': chat_id}, projection)

        # 将 MongoDB 的 _id 字段转换为标准的 id 字段
        return ChatCore.load_from_dict(self._change_id(chat))

    def get_messages(self, chat_id, limit=10) -> list[MessageCore]:
        # 确定 projection
        projection = {} if limit == -1 else {'messages': {'$slice': -limit}}

        # 执行查询
        chat = self.chats.find_one({'_id': chat_id}, projection)

        # 使用列表推导式构建 messages 列表
        messages = [MessageCore.load_from_dict({**msg, 'chat_id': chat_id})
                    for msg in chat['messages']]
        return messages

    def get_runs(self, chat_id: str, limit=10) -> list[RunCore]:
        # 查询 chat 中的 runs
        projection = {} if limit == -1 else {'runs': {'$slice': -limit}}

        chat = self.chats.find_one({'_id': chat_id}, projection)
        runs = [RunCore.load_from_dict({**run, 'chat_id': chat_id})
                for run in chat['runs']]
        log.debug(f"Retrieved {len(runs)} runs for chat {chat_id}")
        return runs

    def add_run(self, chat_id) -> RunCore:
        # 创建一个新的 run
        run_id = gen_id_for_run()
        run = {
            'id': run_id,
            'chat_id': chat_id,
            'created': int(time.time()),
            'status': 'running',
        }
        self.chats.update_one({'_id': chat_id}, {'$push': {'runs': run}})
        return RunCore.load_from_dict(run)

    def update_run(self, chat_id, run_id, status, steps) -> int:
        # 构建查询条件：chat_id 和 run_id
        query = {'_id': chat_id, 'runs.id': run_id}

        # 构建更新语句：根据 new_status 和 new_steps 是否提供来动态构建
        update = {'$set': {}}
        if status is not None:
            update['$set']['runs.$.status'] = status
        if steps is not None:
            update['$set']['runs.$.steps'] = steps

        # 执行更新操作
        result = self.chats.update_one(query, update)
        return result.modified_count


    def get_run(self, chat_id: str, run_id: str) -> RunCore or None:
        # 查询条件：chat_id 和 run_id
        query = {'_id': chat_id, 'runs.id': run_id}

        # 仅选择 runs 字段
        projection = {'runs.$': 1}
        # log.debug(f"query: {query}, projection: {projection}")
        # 执行查询
        chat = self.chats.find_one(query, projection)

        if 'runs' not in chat or len(chat['runs']) == 0:
            log.warning(f"No run found for chat {chat_id}")
            return None

        run = chat['runs'][0]
        return RunCore.load_from_dict({**run, 'chat_id': chat_id})

    def delete_chat(self, chat_id) -> int:
        result = self.chats.delete_one({'_id': chat_id})
        return result.deleted_count

    def only_for_test_clear_all(self):
        self.chats.delete_many({})

    def close(self):
        self.client.close()


chat_dao = ChatDAO(mongodb_client=chat_mongodb, dbname=config.mongodb_dbname)
