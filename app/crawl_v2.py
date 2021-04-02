from selenium import webdriver

from app.utils import parse_amount
from .pages import StocksSearchPage, StocksResultsPage


driver = webdriver.Chrome()

driver.get('https://finance.yahoo.com/screener/unsaved/35d14b15-ff32-4508-90e7-fca42aa45588?dependentField=sector&dependentValues=')

results_page = StocksResultsPage(driver)


# results = results_page.get_current_results()
#
# for result in results:
#     result['price_intraday2'] = parse_amount(result['price_intraday'])
#
# print(*results, sep='\n')

# filter_page = StocksSearchPage(driver)
#
# filter_page.open()
# filter_page.clear_default_selection()
# regions = filter_page.open_regions_dropdown()
#
# regions['Argentina'].toggle()
#
# results_page = filter_page.search_stocks()
#
# results_page.set_rows_per_page(100)
