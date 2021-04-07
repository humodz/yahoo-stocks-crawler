import os
from datetime import timedelta
from functools import lru_cache
from typing import List

from pydantic import BaseSettings, RedisDsn


class Settings(BaseSettings):
    webdriver_args: List[str] = ['--headless']
    cache_ttl: timedelta = timedelta(minutes=3, seconds=13)
    redis_url: RedisDsn = 'redis://localhost:6379/0'


@lru_cache()
def get_settings():
    env_file = os.environ.get('DOTENV_FILE', '.env')

    if env_file != '' and not os.path.exists(env_file):
        raise ValueError('File specified by DOTENV_FILE does not exist')

    return Settings(_env_file=env_file)


if __name__ == '__main__':
    # Run with "python -m app.settings" to check what values are loaded
    print(get_settings().dict())
