from fastapi import Depends

from .cache import Cache, CacheKey
from app.errors import InvalidRegion
from app.pages import StocksSearchPage
from app.settings import get_settings, Settings
from app.utils import ChromeDriver


class Crawler:
    def __init__(
            self,
            settings: Settings = Depends(get_settings),
            cache: Cache = Depends(Cache),
    ):
        self.settings = settings.webdriver_args
        self.cache = cache

    def get_regions(self):
        with ChromeDriver(self.settings) as driver:
            search_form = StocksSearchPage(driver)
            search_form.open()
            regions_dict = search_form.open_regions_dropdown()
            return list(regions_dict.keys())

    def get_stocks(self, region: str):
        cached_regions = self.cache.get(CacheKey.regions)

        if cached_regions is not None and region not in cached_regions:
            raise InvalidRegion(region)

        with ChromeDriver(self.settings) as driver:
            search_form = StocksSearchPage(driver)
            search_form.open()

            regions = search_form.open_regions_dropdown()
            self.cache.set(CacheKey.regions, list(regions.keys()))

            if region not in regions:
                raise InvalidRegion(region)

            regions[region].toggle()

            results_page = search_form.search_stocks()
            results_page.set_rows_per_page(100)

            return list(results_page.get_all_results())
