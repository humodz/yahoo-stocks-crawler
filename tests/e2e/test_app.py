from starlette.testclient import TestClient

from tests.utils import Any, ListOf, DictOf


def test_hello(client: TestClient):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'hello world'}


def test_regions(client):
    response = client.get('/regions')
    body = response.json()

    assert response.status_code == 200

    assert body == {
        'regions': ListOf(Any(str))
    }

    assert 'Brazil' in body['regions']
    assert 'United States' in body['regions']

    # These are used in the following tests
    assert 'Bahrain' in body['regions']
    assert 'Qatar' in body['regions']


def test_stocks(client: TestClient):
    response = client.get('/stocks', params={'region': 'Qatar'})
    body = response.json()

    assert response.status_code == 200
    assert body == DictOf(
        key=Any(str),
        value={
            'name': Any(str),
            'symbol': Any(str),
            'price': Any(str),
        }
    )


# If the region is invalid, return an error
def test_stocks_invalid_region(client: TestClient):
    response = client.get('/stocks', params={'region': 'Brazzil'})

    assert response.status_code == 400
    assert response.json() == {
        'detail': {
            'code': 'INVALID_REGION',
            'message': Any(str),
        }
    }


# If there are no results for a region, should return an empty dict without error
def test_stocks_zero_results(client: TestClient):
    response = client.get('/stocks', params={'region': 'Bahrain'})
    body = response.json()

    assert response.status_code == 200
    assert type(body) == dict
    assert len(body) == 0
