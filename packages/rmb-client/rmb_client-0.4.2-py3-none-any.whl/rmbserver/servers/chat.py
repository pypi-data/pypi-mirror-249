from rmbserver.servers.base import api, auth, Resource, request
from rmbserver.analysis.managers import ChatManager
from rmbserver.log import log
from rmbserver.exceptions import ParameterError

# 定义命名空间
ns_chat = api.namespace('chats', description='聊天操作')


@ns_chat.route('/')
class ChatList(Resource):
    @auth.login_required
    def get(self):
        """
        查询所有的对话
        """
        return [chat.to_dict() for chat in ChatManager.get_all_chats(limit=100)]

    @ns_chat.doc(params={
        'datasource_ids': '数据源 ID 列表，用半角逗号分隔'
    })
    @auth.login_required
    def post(self):
        """
        创建对话
        """
        data = request.json
        datasource_ids = data['datasource_ids']  # 接收数据源 ID 列表
        chat = ChatManager.create_chat(datasource_ids)
        log.info(f"Chat created: {chat}")
        return chat.to_dict(), 201



@ns_chat.route('/<string:chat_id>')
@ns_chat.doc(params={
    'chat_id': '对话 ID'
})
class Chat(Resource):
    @auth.login_required
    def get(self, chat_id):
        """
        查询对话
        """
        mgr = ChatManager(chat_id)
        log.info(f"Chat found: {mgr.chat}")
        return mgr.chat.to_dict(), 200

    @ns_chat.doc(params={
        'chat_id': '对话 ID',
        'question': '问题'
    })
    @auth.login_required
    def post(self, chat_id):
        """
        提问
        """
        data = request.json
        question = data['question']
        mgr = ChatManager(chat_id)
        answer = mgr.answer_question(question)
        log.info(f"答案已生成！ {mgr.chat} \n问题：{question} \n答案：{answer}")
        return answer.to_dict(), 201

    @auth.login_required
    def delete(self, chat_id):
        """
        删除某个对话，以及对话中的所有历史消息和AI执行结果
        """
        mgr = ChatManager(chat_id)
        mgr.chat.delete()
        log.info(f"Chat deleted: {chat_id}")
        return {'message': f'Chat {chat_id} deleted'}, 200



@ns_chat.route('/<string:chat_id>/messages')
class ChatMessages(Resource):
    @ns_chat.doc(params={
        'chat_id': '对话 ID',
        'limit': '要检索的消息数量，可选，默认为 10 条'
    })
    @auth.login_required
    def get(self, chat_id):
        """
        查询所有的消息
        """
        limit = request.args.get('limit', 10)
        try:
            limit = int(limit)
        except ValueError:
            raise ParameterError(f"Invalid limit value: {limit}")

        mgr = ChatManager(chat_id)
        messages = mgr.chat.messages(limit=limit)
        return [message.to_dict() for message in messages], 200

    @ns_chat.doc(params={
        'chat_id': '对话 ID',
        'content': '文本消息'
    })
    @auth.login_required
    def post(self, chat_id):
        """
        发送消息
        """
        data = request.json
        content = data['content']
        mgr = ChatManager(chat_id)
        message = mgr.chat.add_message('human', content=content)
        log.info(f"Message added: {message} in {mgr.chat}")
        return message.to_dict(), 201



@ns_chat.route('/<string:chat_id>/runs')
@ns_chat.doc(params={
    'chat_id': '对话 ID'
})
class ChatRuns(Resource):
    @auth.login_required
    def get(self, chat_id):
        """
        获取所有的AI执行结果
        """
        mgr = ChatManager(chat_id)
        runs = mgr.chat.runs()
        log.info(f"Runs found: {runs} in {mgr.chat}")
        return [run.to_dict() for run in runs], 200

    @auth.login_required
    def post(self, chat_id):
        """
        使用AI进行回复
        """
        mgr = ChatManager(chat_id)
        run = mgr.create_run()
        log.info(f"Run created: {run} in {mgr.chat}")
        return run.to_dict(), 201



@ns_chat.route('/<string:chat_id>/runs/<string:run_id>')
@ns_chat.doc(params={
    'chat_id': '对话 ID',
    'run_id': '运行 ID'
})
class ChatRun(Resource):

    @auth.login_required
    def get(self, chat_id, run_id):
        """
        获取某次AI执行结果
        """
        mgr = ChatManager(chat_id)
        run = mgr.chat.get_run(run_id)
        log.info(f"Run found: {run} in {mgr.chat}")
        return run.to_dict(), 200

    @auth.login_required
    def post(self, chat_id, run_id):
        """
        终止某次AI执行
        """
        action = request.json['action']
        if action == 'cancel':
            mgr = ChatManager(chat_id)
            mgr.chat.cancel_run(run_id)
            log.info(f"Run cancelled: {run_id} in {mgr.chat}")

        else:
            raise ParameterError(f"Invalid action: {action}")
        return {'message': f'Run {run_id} cancelled'}, 200
