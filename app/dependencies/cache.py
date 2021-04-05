import json
from functools import wraps

from fastapi import Depends
from pydantic import RedisDsn
from redis import Redis

from app.settings import get_settings


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


class Cache:
    redis: Redis
    expiration_ms: float

    def __init__(
            self,
            redis=Depends(RedisBackend.inject),
            settings=Depends(get_settings),
    ):
        self.redis = redis
        self.expiration_ms = settings.cache_ttl_ms

    def set(self, key, value, expiration_ms=None):
        if expiration_ms is None:
            expiration_ms = self.expiration_ms

        serialized = json.dumps(value)
        self.redis.set(key, serialized, px=expiration_ms)
        return value

    def get(self, key):
        return self.redis.get(key)

    def decorate(self, key):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cached = self.get(key)

                if cached is not None:
                    return json.loads(cached)

                result = func(*args, **kwargs)
                return self.set(key, result)
            return wrapper
        return decorator
