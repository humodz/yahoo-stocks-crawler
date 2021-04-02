from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from .base_page import BasePage


class StocksResultsPage(BasePage):
    # class TableColumns:
    #     symbol = 0
    #     name = 1
    #     price_intraday = 2
    #     change = 3
    #     change_percent = 4
    #     volume = 5
    #     average_volume = 6
    #     market_capitalization = 7
    #     price_yield_ratio = 8

    class Locators:
        open_rows_per_page = (By.CSS_SELECTOR, '#scr-res-table > div:nth-child(2) [data-test=select-container]')
        rows_per_page_options = (By.CSS_SELECTOR, '#scr-res-table [data-test=showRows-select-menu] > *')
        next_page_button = (By.CSS_SELECTOR, '#scr-res-table > div:nth-child(2) > button:nth-child(4)')
        loading_overlay_present = (By.CSS_SELECTOR, '#scr-res-table:nth-child(3)')
        loading_overlay_not_present = (By.CSS_SELECTOR, '#scr-res-table:nth-child(2)')
        result_rows = (By.CSS_SELECTOR, '#scr-res-table tbody tr')
        table_cell = (By.CSS_SELECTOR, 'td')

    def get_current_results(self):
        column_names = ['symbol', 'name', 'price_intraday']

        def row_to_dict(row):
            cols = self.find_all(root=row, locator=self.Locators.table_cell)
            values = [col.get_attribute('innerText') for col in cols]
            values_dict = {key: value for key, value in zip(column_names, values)}
            return values_dict

        rows = self.find_all(self.Locators.result_rows)
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

    def has_next_page(self):
        return self.find_one(self.Locators.next_page_button).is_enabled()

    def next_page(self):
        next_button = self.find_one(self.Locators.next_page_button)
        next_button.click()
        self.wait_pagination()

    def wait_pagination(self):
        self.wait_until(ec.presence_of_element_located(self.Locators.loading_overlay_present))
        self.wait_until(ec.presence_of_element_located(self.Locators.loading_overlay_not_present))
