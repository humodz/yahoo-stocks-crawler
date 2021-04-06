"""
    Globally available fixtures.
    https://docs.pytest.org/en/stable/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session
"""

import pytest
from starlette.testclient import TestClient

from app.dependencies import RedisBackend
from app.main import app


@pytest.fixture(scope='session')
def client():
    # The "with" statement is required for app.on_event to run
    # https://fastapi.tiangolo.com/advanced/testing-events
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def redis_cleanup_every_test(client: TestClient):
    redis = RedisBackend.inject()
    redis.flushdb()
    yield
    redis.flushdb()

