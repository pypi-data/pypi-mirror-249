import sys
from py2neo import Graph
from qdrant_client import QdrantClient
from pymongo import MongoClient
from urllib.parse import quote_plus
from rmbserver import config
from rmbserver.log import log


def get_graph_db():
    # 存储IDC元数据的图数据库
    try:
        log.info(f"连接Neo4j数据库：{config.neo4j_address}")
        return Graph(
            config.neo4j_address,
            name=config.neo4j_dbname,
            user=config.neo4j_username,
            password=config.neo4j_password
        )
    except Exception as e:
        log.error(f"连接Neo4j数据库失败：{e}")
        sys.exit(1)


def get_vector_db():
    try:
        if config.qdrant_address:
            log.info(f"连接Qdrant数据库服务：{config.qdrant_address}")
            return QdrantClient(
                url=config.qdrant_address
            )
        else:
            log.info(f"连接本地Qdrant数据库文件：{config.qdrant_local_file_path}")
            return QdrantClient(
                path=config.qdrant_local_file_path
            )
    except Exception as e:
        log.error(f"连接Qdrant数据库失败：{e}")
        sys.exit(1)


def get_mongo_db():
    try:
        log.info(f"连接MongoDB数据库：{config.mongodb_address}")
        mongo_uri = "mongodb://%s:%s@%s" % (
            quote_plus(config.mongodb_username),
            quote_plus(config.mongodb_password),
            config.mongodb_address
        )

        return MongoClient(mongo_uri)
    except Exception as e:
        log.error(f"连接MongoDB数据库失败：{e}")
        sys.exit(1)



# Service
service_graph_db = get_graph_db()

# Meta
meta_graph_db = service_graph_db
meta_vector_db = get_vector_db()

# Chat
chat_mongodb = get_mongo_db()
chat_mongodb_db = chat_mongodb[config.mongodb_dbname]
