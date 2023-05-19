import redis
import os
from dotenv import load_dotenv

# 設定ファイルの読み込み
load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

class RedisMemory:
    def __init__(self):
        redis_host = REDIS_HOST
        redis_port = REDIS_PORT
        redis_password = REDIS_PASSWORD
        self.dimention = 1536
        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=0,
        )

        # 接続確認
        try:
            self.redis.ping()
        except redis.ConnectionError as e:
            print("Failed to connect Redis.")

            