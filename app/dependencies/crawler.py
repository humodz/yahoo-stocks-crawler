from app.pages import StocksSearchPage
from app.utils import ChromeDriver


class InvalidRegion(Exception):
    def __init__(self, region):
        super().__init__(f'Invalid region: {region}')
        self.region = region


class Crawler:
    def __init__(self):
        # self.settings = None
        self.settings = [
            '--headless'
        ]

    def get_regions(self):
        with ChromeDriver(self.settings) as driver:
            search_form = StocksSearchPage(driver)
            search_form.open()
            regions_dict = search_form.open_regions_dropdown()
            return list(regions_dict.keys())

    def get_stocks(self, region: str):
        with ChromeDriver(self.settings) as driver:
            search_form = StocksSearchPage(driver)
            search_form.open()

            regions = search_form.open_regions_dropdown()

            if region not in regions:
                raise InvalidRegion(region)

            regions[region].toggle()

            results_page = search_form.search_stocks()
            results_page.set_rows_per_page(100)

            return list(results_page.get_all_results())
