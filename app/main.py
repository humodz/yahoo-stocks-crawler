from fastapi import FastAPI, Depends

from app.dependencies.crawler import Crawler
from app.utils import parse_amount


app = FastAPI()


@app.get('/')
def hello_world():
    return {
        'message': 'hello world'
    }


@app.get('/regions')
def get_regions(crawler: Crawler = Depends(Crawler)):
    '''
        Returns a list of valid regions to fetch stocks.
    '''

    regions = crawler.get_regions()
    return {
        'regions': regions
    }


@app.get('/stocks')
def get_stocks(region: str, crawler: Crawler = Depends(Crawler)):
    '''
        Returns a list of stock prices for the given region.
    '''

    raw_results = crawler.get_stocks(region)

    # Always show 2 decimal places
    currency = '{:.2f}'.format

    results = {
        item['Symbol']: {
            'symbol': item['Symbol'],
            'name': item['Name'],
            'price': currency(parse_amount(item['Price (Intraday)'])),
        }
        for item in raw_results
    }

    return results

