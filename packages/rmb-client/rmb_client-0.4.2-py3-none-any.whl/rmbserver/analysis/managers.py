import time
from rmbserver.log import log
from rmbserver.analysis.chat import Chat
from rmbserver.ai.chatagent import ChatAgentManager
from rmbserver.ai.generations import ai_generate
from rmbcommon.models import BIAnswer
from rmbserver.ai.prompts.agent import PROMPT_FORMAT_AGENT_FINAL_ANSWER


class ChatManager:
    def __init__(self, chat_id: str):
        self.chat = Chat.get(chat_id)

    @staticmethod
    def create_chat(datasource_ids: list[str]) -> Chat:
        """
        Create a chat
        """
        return Chat.create(datasource_ids)

    @staticmethod
    def get_all_chats(limit=100) -> list[Chat]:
        """
        Get all chats
        """
        return Chat.list(limit=limit)

    def create_run(self):
        # new a run
        _run = self.chat.add_run()

        # make a run sync
        # TODO
        return _run

    def answer_question(self, question: str):
        chat_agent = ChatAgentManager(self.chat)
        # time counter
        _begin = time.time()
        answer_str = chat_agent.query(question)
        _end = time.time()
        elapsed_time = int(_end - _begin)

        log.debug(f"Loading answer: {answer_str}, elapsed: {elapsed_time} s.")
        answer_json = ai_generate(
            "FORMAT_AGENT_FINAL_ANSWER",
            PROMPT_FORMAT_AGENT_FINAL_ANSWER,
            origin_answer=answer_str,
            elapsed_time=elapsed_time
        )
        answer = BIAnswer.load_from_dict(answer_json)

        # add a message
        self.chat.add_message(role='human', content=question)
        self.chat.add_message(role='ai', content=answer.to_dict())

        return answer
