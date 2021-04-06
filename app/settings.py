import os
from functools import lru_cache
from typing import List

from pydantic import BaseSettings, Field, validator, RedisDsn

from app.utils import parse_duration_to_ms


class Settings(BaseSettings):
    webdriver_args: List[str] = ['--headless']
    cache_ttl_ms: int = Field('3m 13s', env='cache_ttl')
    redis_url: RedisDsn = 'redis://localhost:6379/0'

    @validator('cache_ttl_ms', pre=True)
    def ttl_is_valid_duration(cls, value):
        return parse_duration_to_ms(value)


@lru_cache()
def get_settings():
    env_file = os.environ.get('DOTENV_FILE', '.env')

    if env_file != '' and not os.path.exists(env_file):
        raise ValueError('File specified by DOTENV_FILE does not exist')

    return Settings(_env_file=env_file)


if __name__ == '__main__':
    # Run with "python -m app.settings" to check what values are loaded
    print(get_settings().dict())
