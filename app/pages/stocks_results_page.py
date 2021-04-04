from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from app.utils import split_into_chunks, benchmark_function
from .base_page import BasePage


class StocksResultsPage(BasePage):
    class Locators:
        floating_header = (By.CSS_SELECTOR, '.YDC-Header')
        request_timeout_indicator = (By.CSS_SELECTOR, '#fin-scr-res-table > :nth-child(2) [data-icon=attention]')
        open_rows_per_page = (By.CSS_SELECTOR, '#scr-res-table > div:nth-child(2) [data-test=select-container]')
        rows_per_page_options = (By.CSS_SELECTOR, '#scr-res-table [data-test=showRows-select-menu] > *')
        next_page_button = (By.CSS_SELECTOR, '#scr-res-table > div:nth-child(2) > button:nth-child(4)')
        loading_overlay_present = (By.CSS_SELECTOR, '#scr-res-table:nth-child(3)')
        loading_overlay_not_present = (By.CSS_SELECTOR, '#scr-res-table:nth-child(2)')
        result_table = (By.CSS_SELECTOR, '#scr-res-table table')
        result_header = (By.CSS_SELECTOR, '#scr-res-table thead th')
        all_cells = (By.CSS_SELECTOR, '#scr-res-table tbody td')

    @benchmark_function
    def get_current_results(self):
        def row_to_dict(cells):
            # Manually iterating and calling .get_attribute in Python: ~20 seconds (100 rows)
            # .execute_script: ~2 seconds (100 rows)
            names_and_values = self.driver.execute_script(
                'return arguments[0].map(e => [e.getAttribute("aria-label"), e.innerText])',
                cells,
            )

            return {name: value for name, value in names_and_values}

        total_columns = len(self.find_all(self.Locators.result_header))
        all_cells = self.find_all(self.Locators.all_cells)
        rows = split_into_chunks(all_cells, total_columns)

        results = [row_to_dict(row) for row in rows]
        return results

    def set_rows_per_page(self, amount):
        allowed_amounts = [25, 50, 100]

        if amount not in allowed_amounts:
            raise RuntimeError(f'Results per page must be one of: {allowed_amounts}')

        self.find_one(self.Locators.open_rows_per_page).click()

        options = self.find_all(self.Locators.rows_per_page_options)
        options[allowed_amounts.index(amount)].click()
        self.wait_pagination()

    @benchmark_function
    def has_next_page(self):
        return self.find_one(self.Locators.next_page_button).is_enabled()

    @benchmark_function
    def next_page(self):
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
            if retry:
                # Using .find_all because it doesn't throw
                if 0 == len(self.find_all(self.Locators.request_timeout_indicator)):
                    # If the error indicator is not present, no idea what happened.
                    raise timed_out

                self._refresh()
                self._hide_floating_header()
                # If it fails again, give up
                self.wait_pagination(retry=False)

    def _refresh(self):
        self.driver.refresh()

    # This is duplicated from stocks_search_page ...
    def _hide_floating_header(self):
        # This header sometimes obscures buttons and causes errors
        header = self.find_one(self.Locators.floating_header)
        self.driver.execute_script('arguments[0].style.display = "none"', header)

    def get_all_results(self):
        yield from self.get_current_results()

        while self.has_next_page():
            self.next_page()
            yield from self.get_current_results()
