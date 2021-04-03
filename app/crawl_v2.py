from selenium import webdriver

from app.utils import parse_amount, ChromeDriver
from .pages import StocksSearchPage

# driver = webdriver.Chrome()

with ChromeDriver(['--headless']) as driver:
# with ChromeDriver() as driver:
    search_form = StocksSearchPage(driver)

    search_form.open()
    search_form.clear_default_selection()
    regions = search_form.open_regions_dropdown()

    regions['Argentina'].toggle()

    results_page = search_form.search_stocks()

    results_page.set_rows_per_page(100)

    #print(*results_page.get_current_results(), sep='\n')


# all_results = list(results_page.get_all_results())
