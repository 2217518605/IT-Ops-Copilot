import redis
import hashlib
import json
from typing import Optional


class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def get_cache_key(self, question: str) -> str:
        """生成问题的缓存key"""

        return f"qa:{hashlib.md5(question.encode()).hexdigest()}"

    def get(self, key: str) -> Optional[str]:
        """获取缓存"""

        return self.redis_client.get(key)

    def set(self, key: str, value: str, expire: int = 300):
        """设置缓存"""

        self.redis_client.setex(key, expire, value)

    def delete_pattern(self, pattern: str):
        """批量删除缓存"""

        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)


# 全局缓存实例
redis_cache = RedisCache()
