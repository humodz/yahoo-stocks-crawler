from typing import List

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout_seconds=30):
        self.driver = driver
        self.timeout = timeout_seconds

    def find_one(self, locator, root=None) -> WebElement:
        if root is None:
            root = self.driver
        return root.find_element(*locator)

    def find_all(self, locator, root=None) -> List[WebElement]:
        if root is None:
            root = self.driver
        return root.find_elements(*locator)

    def wait_until(self, what):
        return WebDriverWait(self.driver, self.timeout).until(what)
