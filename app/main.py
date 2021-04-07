from fastapi import FastAPI, Depends, HTTPException

from app.dependencies import Crawler, RedisBackend, Cache, InvalidRegion
from app.model import RegionsResponse, StockItem, StocksResponse
from app.settings import get_settings

app = FastAPI()


@app.get('/')
def hello_world():
    return {
        'message': 'hello world'
    }


@app.get('/regions', response_model=RegionsResponse)
def get_regions(
        crawler: Crawler = Depends(Crawler),
        cache: Cache = Depends(Cache),
):
    """
    List valid regions to fetch stocks from.
    """
    @cache.decorate('cache:regions')
    def get_regions_with_cache():
        return crawler.get_regions()

    regions = get_regions_with_cache()
    return {
        'regions': regions
    }


@app.get(
    '/stocks',
    response_model=StocksResponse,
    responses={
        400: {'description': 'Invalid Region'}
    }
)
def get_stocks(
        region: str,
        crawler: Crawler = Depends(Crawler),
        cache: Cache = Depends(Cache)
):
    """
    List stock prices for the given region.<br>
    Returns an object whose keys are the stock symbols.<br>
    Note: The Yahoo finance screener can only return up to 10000 results.
    """
    @cache.decorate(f'cache:stocks:{region}')
    def get_stocks_with_cache():
        try:
            raw_results = crawler.get_stocks(region)
        except InvalidRegion as error:
            return {
                'status': 400,
                'error': {'code': 'INVALID_REGION', 'message': str(error)}
            }

        return {
            'data': {
                item['Symbol']: StockItem.from_table_row(item).dict()
                for item in raw_results
            }
        }

    result = get_stocks_with_cache()

    if 'error' in result:
        raise HTTPException(
            status_code=result['status'],
            detail=result['error'],
        )

    return result['data']


@app.on_event('startup')
def initialize():
    settings = get_settings()
    RedisBackend.connect(settings.redis_url)
