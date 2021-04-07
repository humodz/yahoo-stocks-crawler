from fastapi import FastAPI, Depends, HTTPException

from app.dependencies import Crawler, RedisBackend, Cache, CacheKey
from app.errors import InvalidRegion
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
    @cache.decorate(CacheKey.regions)
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
    @cache.decorate(CacheKey.stocks(region))
    def get_stocks_with_cache():
        try:
            results = crawler.get_stocks(region)
        except InvalidRegion as error:
            raise HTTPException(
                status_code=400,
                detail={'code': 'INVALID_REGION', 'message': str(error)},
            )

        return {
            item['Symbol']: StockItem.from_table_row(item).dict()
            for item in results
        }

    return get_stocks_with_cache()


@app.on_event('startup')
def initialize():
    settings = get_settings()
    RedisBackend.connect(settings.redis_url)
