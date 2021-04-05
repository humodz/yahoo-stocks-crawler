'''
    Testing script for the crawler
'''


from app.utils import ChromeDriver, benchmark_function
from .pages import StocksSearchPage

b = benchmark_function

with ChromeDriver(['--headless'], keep_open=False) as driver:
    search_form = StocksSearchPage(driver)

    b(search_form.open)()
    regions = b(search_form.open_regions_dropdown)()

    regions['Qatar'].toggle()

    results_page = search_form.search_stocks()

    b(results_page.set_rows_per_page)(100)

    all_results = b(list)(results_page.get_all_results())

    print(len(all_results))

