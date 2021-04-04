from fastapi import FastAPI, Depends, HTTPException

from app.dependencies import Crawler
from app.dependencies.crawler import InvalidRegion
from app.model import RegionsResponse, StockItem, StocksResponse

app = FastAPI()


@app.get('/')
def hello_world():
    return {
        'message': 'hello world'
    }


@app.get('/regions', response_model=RegionsResponse)
def get_regions(crawler: Crawler = Depends(Crawler)):
    '''
        List valid regions to fetch stocks from.
    '''

    regions = crawler.get_regions()
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
def get_stocks(region: str, crawler: Crawler = Depends(Crawler)):
    '''
        List stock prices for the given region.<br>
        Returns an object whose keys are the stock symbols.
    '''

    try:
        raw_results = crawler.get_stocks(region)
    except InvalidRegion as error:
        raise HTTPException(status_code=400, detail={
            'code': 'INVALID_REGION',
            'message': str(error),
        })

    return {
        item['Symbol']: StockItem.from_table_row(item)
        for item in raw_results
    }

