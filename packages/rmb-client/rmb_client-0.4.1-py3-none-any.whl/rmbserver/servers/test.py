from rmbserver.servers.base import api, auth, Resource
from rmbserver.log import log
from rmbserver.brain.dao_meta import meta_dao
from rmbserver.analysis.dao_chat import chat_dao


ns_test = api.namespace('tests', description='测试操作')



@ns_test.route('/clear_data/<string:scope>')
class TestClearAll(Resource):

    @auth.login_required
    @ns_test.doc(params={
        'scope': '清空数据的范围：all|brain|chat'
    })
    def post(self, scope):
        """
        清空数据
        """
        if scope == 'all':
            log.info(f"Clearing all brain&chat data...")
            meta_dao.only_for_test_clear_all()
            chat_dao.only_for_test_clear_all()
            return {'message': 'All brain&chat data cleared'}, 200
        elif scope == 'brain':
            log.info(f"Clearing all brain data...")
            meta_dao.only_for_test_clear_all()
            return {'message': 'All brain data cleared'}, 200
        elif scope == 'chat':
            log.info(f"Clearing all chat data...")
            chat_dao.only_for_test_clear_all()
            return {'message': 'All chat data cleared'}, 200
        else:
            return {'message': 'nothing cleared'}, 200

