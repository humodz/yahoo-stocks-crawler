from fastapi import FastAPI, Depends

from app.dependencies import Crawler
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


@app.get('/stocks', response_model=StocksResponse)
def get_stocks(region: str, crawler: Crawler = Depends(Crawler)):
    '''
        List stock prices for the given region.<br>
        Returns an object whose keys are the stock symbols.
    '''

    raw_results = crawler.get_stocks(region)

    return {
        item['Symbol']: StockItem.from_table_row(item)
        for item in raw_results
    }

