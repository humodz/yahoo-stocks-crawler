from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from .base_page import BasePage
from .stocks_results_page import StocksResultsPage


class StocksSearchPage(BasePage):
    class Locators:
        default_selected_region = (By.CSS_SELECTOR, '#screener-criteria .filterItem button')
        show_regions_button = (
            By.CSS_SELECTOR, '#screener-criteria [data-test=field-section]:first-child .filterAdd > div > div',
        )
        region_checkboxes = (By.CSS_SELECTOR, '#dropdown-menu label')
        find_stocks_button = (By.CSS_SELECTOR, 'button[data-test=find-stock]')
        results_table = (By.CSS_SELECTOR, '#fin-scr-res-table table')

    class Region:
        def __init__(self, element):
            self.name = element.get_attribute('innerText')
            self.element = element

        def toggle(self):
            self.element.click()

    def open(self):
        self.driver.get('https://finance.yahoo.com/screener/new')

    def clear_default_selection(self):
        self.find_one(self.Locators.default_selected_region).click()

    def open_regions_dropdown(self):
        self.find_one(self.Locators.show_regions_button).click()
        region_checkboxes = self.find_all(self.Locators.region_checkboxes)

        regions_by_name = {
            element.get_attribute('innerText'): self.Region(element)
            for element in region_checkboxes
        }

        return regions_by_name

    def search_stocks(self):
        button = self.wait_until(ec.element_to_be_clickable(self.Locators.find_stocks_button))
        button.click()
        self.wait_until(ec.presence_of_element_located(self.Locators.results_table))

        results_page = StocksResultsPage(self.driver, self.timeout)
        return results_page
