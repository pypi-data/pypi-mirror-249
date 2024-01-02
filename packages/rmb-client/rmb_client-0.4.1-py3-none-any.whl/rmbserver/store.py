import oss2
import sys
from rmbserver import config
from rmbserver.log import log


# 配置阿里云OSS的访问密钥和终端地址
try:
    oss_auth = oss2.Auth(config.oss_access_key_id, config.oss_access_key_secret)
    oss_bucket = oss2.Bucket(oss_auth, config.oss_endpoint, config.oss_bucket_name)
except:
    log.error("OSS 配置错误，请检查！")
    sys.exit(1)

