import re

import pytest

from app.pages import StocksSearchPage
from app.settings import get_settings
from app.utils import ChromeDriver


@pytest.mark.want
def test_yahoo_finance_max_results():
    """
        Validates that the website can't fetch results past YAHOO_FINANCE_MAX_RESULTS
        If this behavior changes, StocksResultsPage will need to be updated
    """
    args = get_settings().webdriver_args

    with ChromeDriver(options=args) as driver:
        search_form = StocksSearchPage(driver)

        search_form.open()
        regions = search_form.open_regions_dropdown()
        regions['United States'].toggle()

        search_page = search_form.search_stocks()
        search_page.set_rows_per_page(100)

        offset = search_page.YAHOO_FINANCE_MAX_RESULTS

        old_url = driver.current_url
        new_url = re.sub(r'offset=\d+', f'offset={offset}', old_url)
        driver.get(new_url)
        search_page.hide_floating_header()

        screener = driver.find_element_by_id('screener-criteria')
        text = screener.text.lower()

        assert 'unable to load screener' in text
