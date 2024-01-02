import os

# 是否开启debug模式
DEBUG = True


# 读取Neo4j 数据库环境变量
# Graph 存储的是 Meta Data
neo4j_username = os.environ.get("NEO4J_USERNAME", 'neo4j')
neo4j_password = os.environ.get("NEO4J_PASSWORD", 'neo4j')
neo4j_dbname = os.environ.get("NEO4J_DBNAME", 'rmb_test')
neo4j_address = os.environ.get("NEO4J_ADDRESS", 'bolt://localhost:7687')

# 读取 MongoDB 环境变量
# MongoDB 存储的是 Chat History
mongodb_username = os.environ.get("MONGODB_USERNAME", 'datamini')
mongodb_password = os.environ.get("MONGODB_PASSWORD", 'datamini')
mongodb_address = os.environ.get("MONGODB_ADDRESS", '127.0.0.1:27017')
mongodb_dbname = os.environ.get("MONGODB_DBNAME", 'rmb_test')


# 读取Qdrant环境变量  如果 qdrant_address 为空，则使用 qdrant_local_file_path
qdrant_address = os.environ.get("QDRANT_ADDRESS", 'http://localhost:6333')
qdrant_local_file_path = os.environ.get("QDRANT_LOCAL_FILE_PATH", '/tmp/rmb_vectors.db')

# 生成的文件存储在OSS上
oss_access_key_id = os.environ.get("OSS_ACCESS_KEY_ID", '')
oss_access_key_secret = os.environ.get("OSS_ACCESS_KEY_SECRET", '')
oss_endpoint = os.environ.get("OSS_ENDPOINT", '')
oss_bucket_name = os.environ.get("OSS_BUCKET_NAME", '')


# 读取OpenAI环境变量
# 用到了JSON FORMAT 因此，必须使用gpt-4-1106-preview及以上版本的模型
openai_model_name = os.environ.get("OPENAI_MODEL_NAME", 'gpt-4-1106-preview')

openai_embedding_model = os.environ.get("OPENAI_EMBEDDING_MODEL", 'text-embedding-ada-002')
openai_embedding_vector_size = 1536
openai_api_key = os.environ.get("OPENAI_API_KEY", '')
openai_proxy = os.environ.get("OPENAI_PROXY", '')
openai_base_url = os.environ.get("OPENAI_BASE_URL", 'https://api.openai.com/v1')
openai_max_token = 4000


# ServerTokens
server_tokens = os.environ.get("RMB_SERVER_TOKENS", 'token1,token2')

