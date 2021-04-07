import re
from itertools import islice

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from app.utils import split_into_chunks, benchmark_function
from .base_page import BasePage


class MaximumResultsExceeded(Exception):
    def __init__(self, max_results):
        super().__init__(f'Yahoo Finance can only display up to {max_results} results')


class StocksResultsPage(BasePage):
    # The screener can't display past 10000 items, after that it always errors with "Unable to load Screener"
    YAHOO_FINANCE_MAX_RESULTS = 10000

    class Locators:
        floating_header = (By.CSS_SELECTOR, '.YDC-Header')
        request_timeout_indicator = (By.CSS_SELECTOR, '#fin-scr-res-table > :nth-child(2) [data-icon=attention]')
        open_rows_per_page = (By.CSS_SELECTOR, '#scr-res-table > div:nth-child(2) [data-test=select-container]')
        rows_per_page_options = (By.CSS_SELECTOR, '#scr-res-table [data-test=showRows-select-menu] > *')
        next_page_button = (By.CSS_SELECTOR, '#scr-res-table > div:nth-child(2) > button:nth-child(4)')
        loading_overlay_present = (By.CSS_SELECTOR, '#scr-res-table:nth-child(3)')
        loading_overlay_not_present = (By.CSS_SELECTOR, '#scr-res-table:nth-child(2)')
        result_information = (By.CSS_SELECTOR, '#fin-scr-res-table > :first-child')
        result_table = (By.CSS_SELECTOR, '#scr-res-table table')
        result_header = (By.CSS_SELECTOR, '#scr-res-table thead th')
        result_cells = (By.CSS_SELECTOR, '#scr-res-table tbody td')

    def get_current_results(self):
        if self.total_results() == 0:
            return []

        def row_to_dict(cells):
            # Manually iterating and calling .get_attribute in Python: ~20 seconds (100 rows)
            # .execute_script: ~2 seconds (100 rows)
            names_and_values = self.driver.execute_script(
                'return arguments[0].map(e => [e.getAttribute("aria-label"), e.innerText])',
                cells,
            )

            return {name: value for name, value in names_and_values}

        total_columns = len(self.find_all(self.Locators.result_header))
        all_cells = self.find_all(self.Locators.result_cells)
        rows = list(split_into_chunks(all_cells, total_columns))

        results = [row_to_dict(row) for row in rows]
        return results

    def set_rows_per_page(self, amount):
        # If the results fit in a single page, the "Show N Rows" dropdown won't exist
        if not self.has_next_page():
            return

        allowed_amounts = [25, 50, 100]

        if amount not in allowed_amounts:
            raise RuntimeError(f'Results per page must be one of: {allowed_amounts}')

        self.find_one(self.Locators.open_rows_per_page).click()

        options = self.find_all(self.Locators.rows_per_page_options)
        options[allowed_amounts.index(amount)].click()
        self.wait_pagination()

    def total_results(self):
        # Some regions have zero results, e.g. Bahrain
        info = self.find_one(self.Locators.result_information).get_property('innerText')
        regexp = re.compile(r'of (\d+) results')
        total = regexp.search(info).group(1)
        return int(total)

    def has_next_page(self):
        # If the results fit in a single page the Next Page button isn't created, but checking if it doesn't exist
        # may cause false positives if the page errors
        info = self.find_one(self.Locators.result_information).get_property('innerText')
        regexp = re.compile(r'\d+-(\d+) of (\d+) results')
        current, total = regexp.search(info).groups()
        return current != total

    def next_page(self):
        # Note: if the results fit in a single page, this button won't exist
        next_button = self.find_one(self.Locators.next_page_button)
        next_button.click()
        self.wait_pagination()

    def wait_pagination(self, retry=True):
        try:
            # Wait a bit for the result table to disappear, to be sure we don't advance too fast.
            # Sometimes the result table doesn't disappear, but if it does, it should take less than 5 secs,
            # so the timeout is fine here.
            self.wait_until(timeout=5, what=ec.invisibility_of_element_located(self.Locators.result_table))
        except TimeoutException:
            pass

        try:
            self.wait_until(ec.visibility_of_element_located(self.Locators.result_table))
        except TimeoutException as timed_out:
            # Sometimes requests time out and the page errors. In that case, refresh and try again one time.
            if not retry and not self.is_present(self.Locators.request_timeout_indicator):
                if f'&offset={self.YAHOO_FINANCE_MAX_RESULTS}' in self.driver.current_url:
                    raise MaximumResultsExceeded(self.YAHOO_FINANCE_MAX_RESULTS)

                # Unknown error
                raise timed_out

            self._refresh()
            # If it fails again, give up
            self.wait_pagination(retry=False)

    def _refresh(self):
        self.driver.refresh()
        self._hide_floating_header()

    # This is duplicated from stocks_search_page ...
    def _hide_floating_header(self):
        # This header sometimes obscures buttons and causes errors
        header = self.find_one(self.Locators.floating_header)
        self.driver.execute_script('arguments[0].style.display = "none !important"', header)

    def get_all_results(self, stop_before_error=True):
        """
        Returns all stocks for the given screener, iterating through the pages
        :param stop_before_error: If False, then it may throw MaximumResultsExceeded
        """
        if stop_before_error:
            return islice(self._get_all_results(), self.YAHOO_FINANCE_MAX_RESULTS)
        else:
            return self._get_all_results()

    def _get_all_results(self):
        yield from self.get_current_results()

        while self.has_next_page():
            self.next_page()
            yield from self.get_current_results()
