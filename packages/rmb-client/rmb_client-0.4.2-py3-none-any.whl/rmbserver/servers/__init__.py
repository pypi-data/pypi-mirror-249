from rmbserver.servers.base import app
from rmbserver.servers.datasource import ns_datasource
from rmbserver.servers.chat import ns_chat
from rmbserver.servers.test import ns_test
from rmbserver.servers.exception_handler import *


__ALL__ = [
    'app',
    'ns_datasource',
    'ns_chat',
    'ns_test'
]
