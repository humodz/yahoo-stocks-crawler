import pytest
from starlette.testclient import TestClient

from tests.utils import Any, ListOf, DictOf


@pytest.mark.e2e
def test_hello(client: TestClient):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'hello world'}


@pytest.mark.e2e
def test_regions(client: TestClient):
    response = client.get('/regions')
    body = response.json()

    assert response.status_code == 200

    assert body == {
        'regions': ListOf(Any(str))
    }

    assert 'Brazil' in body['regions']
    assert 'United States' in body['regions']

    # These are used in the next tests, validate they still exist
    assert 'Bahrain' in body['regions']
    assert 'Qatar' in body['regions']
    assert 'Belgium' in body['regions']


# Qatar has one page of results
# Belgium has more than one page
@pytest.mark.e2e
@pytest.mark.parametrize('region', ['Qatar', 'Belgium'])
def test_stocks(client: TestClient, region: str):
    print('HELLO', region)
    response = client.get('/stocks', params={'region': region})
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


@pytest.mark.e2e
def test_stocks_region_missing(client: TestClient):
    response = client.get('/stocks')
    assert response.status_code == 422

# If the region is invalid, return an error
@pytest.mark.e2e
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
# Bahrain has no results
@pytest.mark.e2e
def test_stocks_zero_results(client: TestClient):
    response = client.get('/stocks', params={'region': 'Bahrain'})
    body = response.json()

    assert response.status_code == 200
    assert type(body) == dict
    assert len(body) == 0
