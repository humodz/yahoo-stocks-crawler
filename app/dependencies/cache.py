import json
from functools import wraps

from fastapi import Depends
from redis import Redis


class RedisBackend:
    redis: Redis = None

    @classmethod
    def inject(cls):
        if cls.redis is None:
            raise RuntimeError('Forgot to establish connection to Redis')
        return cls.redis

    @classmethod
    def connect(cls):
        # TODO configuration
        cls.redis = Redis()


class Cache:
    redis: Redis
    expiration_ms: float

    def __init__(self, redis=Depends(RedisBackend.inject)):
        self.redis = redis
        # TODO configuration
        self.expiration_ms = (60 * 3 + 13) * 1000

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
