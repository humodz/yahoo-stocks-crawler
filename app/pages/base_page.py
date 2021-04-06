from typing import List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    driver: WebDriver
    timeout: int

    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.timeout = timeout

    def find_one(self, locator, root=None) -> WebElement:
        if root is None:
            root = self.driver
        return root.find_element(*locator)

    def find_all(self, locator, root=None) -> List[WebElement]:
        if root is None:
            root = self.driver
        return root.find_elements(*locator)

    def wait_until(self, what, timeout=None):
        if timeout is None:
            timeout = self.timeout

        return WebDriverWait(self.driver, timeout).until(what)

    def wait_until_not(self, what, timeout=None):
        if timeout is None:
            timeout = self.timeout

        return WebDriverWait(self.driver, timeout).until_not(what)
