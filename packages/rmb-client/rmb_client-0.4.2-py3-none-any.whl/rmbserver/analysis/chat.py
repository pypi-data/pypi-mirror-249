
from rmbcommon.models import ChatCore, RunCore
from rmbserver.analysis.dao_chat import chat_dao
from rmbserver.brain.dao_service import service_dao
from rmbserver.brain.datasource import DataSource
from rmbserver.exceptions import ChatNotFound, DataSourceNotFound
from rmbserver.log import log


class Chat(ChatCore):

    @classmethod
    def get(cls, chat_id: str):
        _chat = chat_dao.get_chat(chat_id)
        if not _chat:
            raise ChatNotFound(f"Chat not found: {chat_id}")
        return cls(**_chat.to_dict())

    @classmethod
    def create(cls, datasource_ids: list[str]) -> ChatCore:
        """
        Create a chat
        """
        invalid_datasource_ids = service_dao.check_datasource_ids(datasource_ids)
        if invalid_datasource_ids:
            raise DataSourceNotFound(f"DataSource not found: {','.join(invalid_datasource_ids)}")

        _chat = chat_dao.create_chat(datasource_ids)
        return cls(**_chat.to_dict())

    @classmethod
    def list(cls, limit=100):
        # 获取所有的对话
        return [cls(**chat.to_dict()) for chat in chat_dao.get_chats(limit=limit)]

    def delete(self):
        delete_count = chat_dao.delete_chat(self.id)
        return delete_count

    def add_message(self, role, content):
        # 添加消息
        return chat_dao.add_message(chat_id=self.id, role=role, content=content)

    def messages(self, limit=10):
        return chat_dao.get_messages(chat_id=self.id, limit=limit)

    def add_run(self):
        return chat_dao.add_run(chat_id=self.id)

    def cancel_run(self, run_id):
        return chat_dao.update_run(chat_id=self.id, run_id=run_id, status='canceled')

    def finished_run(self, run_id):
        return chat_dao.update_run(chat_id=self.id, run_id=run_id, status='finished')

    def runs(self, limit=10):
        return chat_dao.get_runs(chat_id=self.id, limit=limit)

    def get_run(self, run_id) -> RunCore:
        # 获取运行状态
        log.debug(f"Retrieved run {run_id} for chat {self.id}")
        return chat_dao.get_run(chat_id=self.id, run_id=run_id)

    @property
    def datasources(self):
        return [DataSource.get(ds_id) for ds_id in self.datasource_ids]

    @property
    def status(self):
        run_status = self.runs()[-1].status
        if run_status == 'running':
            return 'replying'
        else:
            return 'idle'

    def answer(self, question):
        self.add_message(role='human', content=question)



if __name__ == '__main__':
    c = Chat.get('chat_3P3myjfTyzR53yBSTGmUil')
    print(c.messages())
    print(c.runs())
