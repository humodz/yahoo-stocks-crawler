from datetime import datetime
from time import time

from fastapi import FastAPI, Depends

from app.pages import StocksSearchPage
from app.utils import ChromeDriver, benchmark_function

data = dict()

class Cache:
    def get(self, key):
        return data.get(key, None)

    def set(self, key, value):
        data[key] = value
        return value


app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello world"}


@app.get('/cache')
def hello_cache(region: str, cache=Depends(Cache)):
    cache_key = f'hello:{region}'
    cached = cache.get(cache_key)

    if cached is not None:
        return cached

    return cache.set(cache_key, {
        "region": region,
        "now": str(datetime.utcnow())
    })


@app.get('/regions')
def get_regions():
    with ChromeDriver(['--headless']) as driver:
        search_form = StocksSearchPage(driver)
        search_form.open()
        regions_dict = search_form.open_regions_dropdown()
        regions = list(regions_dict.keys())
        return {
            'regions': regions
        }


@app.get("/stocks")
def get_stocks(region: str):
    with ChromeDriver(['--headless']) as driver:
        search_form = StocksSearchPage(driver)
        search_form.open()

        regions = search_form.open_regions_dropdown()
        regions[region].toggle()

        results_page = search_form.search_stocks()
        results_page.set_rows_per_page(100)

        results = list(results_page.get_all_results())

        return {
            'results': results,
        }

