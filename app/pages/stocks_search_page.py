from typing import Dict

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from .base_page import BasePage
from .stocks_results_page import StocksResultsPage


class StocksSearchPage(BasePage):
    class Locators:
        floating_header = (By.CSS_SELECTOR, '.YDC-Header')
        default_selected_region = (By.CSS_SELECTOR, '#screener-criteria .filterItem button')
        show_regions_button = (
            By.CSS_SELECTOR, '#screener-criteria [data-test=field-section]:first-child .filterAdd > div > div',
        )
        region_checkboxes = (By.CSS_SELECTOR, '#dropdown-menu label')
        find_stocks_button = (By.CSS_SELECTOR, 'button[data-test=find-stock]')
        results_indicator = (By.CSS_SELECTOR, '#fin-scr-res-table [data-test=table-toolbar]')

    class Checkbox:
        def __init__(self, name, element):
            self.name = name
            self.element = element

        def toggle(self):
            self.element.click()

    def open(self):
        self.driver.get('https://finance.yahoo.com/screener/new')

        self._hide_floating_header()
        self._clear_default_selection()

    def _hide_floating_header(self):
        # This header sometimes obscures buttons and causes errors
        header = self.find_one(self.Locators.floating_header)
        self.driver.execute_script('arguments[0].style.display = "none"', header)

    def _clear_default_selection(self):
        self.find_one(self.Locators.default_selected_region).click()

    def open_regions_dropdown(self) -> Dict[str, Checkbox]:
        self.find_one(self.Locators.show_regions_button).click()
        region_checkboxes = self.find_all(self.Locators.region_checkboxes)

        # Manually iterating and calling .get_attribute in Python: ~0.3s
        # .execute_script: ~0.006s
        region_names = self.driver.execute_script('return arguments[0].map(e => e.innerText)', region_checkboxes)

        return {
            name: self.Checkbox(name, checkbox)
            for name, checkbox in zip(region_names, region_checkboxes)
        }

    def search_stocks(self):
        button = self.wait_until(ec.element_to_be_clickable(self.Locators.find_stocks_button))
        button.click()
        self.wait_until(ec.presence_of_element_located(self.Locators.results_indicator))

        return StocksResultsPage(self.driver, self.timeout)
