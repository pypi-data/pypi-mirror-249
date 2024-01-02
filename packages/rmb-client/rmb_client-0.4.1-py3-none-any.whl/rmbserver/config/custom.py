import os

# 是否开启debug模式
DEBUG = True


# 读取Neo4j 数据库环境变量
# Graph 存储的是 Meta Data
neo4j_username = os.environ.get("NEO4J_USERNAME", 'neo4j')
neo4j_password = os.environ.get("NEO4J_PASSWORD", 'Pass1234')
neo4j_dbname = os.environ.get("NEO4J_DBNAME", 'leletest')
neo4j_address = os.environ.get("NEO4J_ADDRESS", 'bolt://127.0.0.1:32768')

# 读取 MongoDB 环境变量
# MongoDB 存储的是 Chat History
mongodb_username = os.environ.get("MONGODB_USERNAME", 'datamini')
mongodb_password = os.environ.get("MONGODB_PASSWORD", 'Pass1234')
mongodb_address = os.environ.get("MONGODB_ADDRESS", 'fbi.chat:27017')
mongodb_dbname = os.environ.get("MONGODB_DBNAME", 'lele_test')


# 读取Qdrant环境变量  如果 qdrant_address 为空，则使用本地文件
qdrant_address = os.environ.get("QDRANT_ADDRESS", 'http://localhost:32772')


# 生成的文件存储在OSS上
oss_access_key_id = os.environ.get("OSS_ACCESS_KEY_ID", '')
oss_access_key_secret = os.environ.get("OSS_ACCESS_KEY_SECRET", '')
oss_endpoint = os.environ.get("OSS_ENDPOINT", 'oss-cn-shanghai.aliyuncs.com')
oss_bucket_name = os.environ.get("OSS_BUCKET_NAME", 'tablebot-gen-files')


openai_api_key = os.environ.get("OPENAI_API_KEY", '')
openai_proxy = os.environ.get("OPENAI_PROXY", 'http://127.0.0.1:8001')

# ServerTokens
server_tokens = os.environ.get("RMB_SERVER_TOKENS", 'token1')
