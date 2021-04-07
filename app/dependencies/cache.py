import json
from functools import wraps
from typing import Optional

from fastapi import Depends
from pydantic import RedisDsn
from redis import Redis

from app.settings import get_settings, Settings


class RedisBackend:
    redis: Redis = None

    @classmethod
    def inject(cls):
        if cls.redis is None:
            raise RuntimeError('Forgot to establish connection to Redis')
        return cls.redis

    @classmethod
    def connect(cls, url: RedisDsn):
        cls.redis = Redis.from_url(url)


class CacheKey:
    regions = 'cache:regions'

    @staticmethod
    def stocks(region):
        return f'cache:stocks:{region}'


class Cache:
    redis: Redis
    expiration_ms: float

    def __init__(
            self,
            redis: Redis = Depends(RedisBackend.inject),
            settings: Settings = Depends(get_settings),
    ):
        self.redis = redis
        self.expiration_ms = int(1000 * settings.cache_ttl.total_seconds())

    def set(self, key: str, value, expiration_ms: Optional[int] = None):
        if expiration_ms is None:
            expiration_ms = self.expiration_ms

        serialized = json.dumps(value)
        self.redis.set(key, serialized, px=expiration_ms)
        return value

    def get(self, key: str):
        raw_value = self.redis.get(key)

        if raw_value is None:
            return None

        return json.loads(raw_value)

    def decorate(self, key: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cached = self.get(key)

                if cached is not None:
                    return cached

                result = func(*args, **kwargs)
                return self.set(key, result)

            return wrapper

        return decorator
