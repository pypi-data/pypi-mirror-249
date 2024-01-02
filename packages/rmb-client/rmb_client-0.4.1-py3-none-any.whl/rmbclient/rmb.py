from rmbclient.models import DataResourceList, ChatList
from rmbclient.api import rmb_api
from rmbcommon.version import VERSION


class ReliableMetaBrain:
    __version__ = VERSION
    version = VERSION

    def __init__(self, api_url='http://127.0.0.1:5000',
                 token='token1', debug=False):
        rmb_api.api_url = api_url
        rmb_api.token = token
        rmb_api.debug = debug

    @property
    def datasources(self):
        return DataResourceList(endpoint="/datasources/")

    @property
    def chats(self):
        return ChatList(endpoint="/chats/")

    def test_clear_all(self):
        return rmb_api.send(endpoint="/tests/clear_data/all", method="POST")

    def test_clear_brain(self):
        return rmb_api.send(endpoint="/tests/clear_data/brain", method="POST")

    def test_clear_chat(self):
        return rmb_api.send(endpoint="/tests/clear_data/chat", method="POST")

