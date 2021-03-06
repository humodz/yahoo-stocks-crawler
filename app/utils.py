import re
from functools import wraps
from time import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Example: +10,000.00M
parse_amount_regexp = re.compile(r'([-+])?((?:\d+,)*\d+(\.\d+)?)([%MBT])?')


def parse_amount(raw_value: str):
    raw_value = raw_value.strip()

    if raw_value == '' or raw_value.upper() == 'N/A':
        return None

    regexp = parse_amount_regexp
    pattern = regexp.fullmatch(raw_value)
    if pattern is None:
        raise ValueError('invalid amount string')

    sign, str_value, _, modifier = pattern.groups()

    result = float(str_value.replace(',', ''))

    if sign == '-':
        result = -result

    if modifier is not None:
        # percent, million, billion, etc
        modifiers = {
            '%': 1 / 100,
            'M': 1000 ** 2,
            'B': 1000 ** 3,
            'T': 1000 ** 4,
        }

        result = result * modifiers[modifier]

    return result


def split_into_chunks(items, chunk_size):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]


def benchmark_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        try:
            return func(*args, **kwargs)
        finally:
            print('benchmark_function:', func.__qualname__, time() - start)

    return wrapper


class ChromeDriver:
    driver: Optional[webdriver.Chrome]

    # Note: if keep_open=True, the browser and driver will keep running on background
    # and need to be killed manually, e.g.: pgrep chrome | xargs kill
    def __init__(self, options=None, keep_open=False):
        self.driver = None
        self.keep_open = keep_open
        self.options = Options()

        if options is not None:
            for option in options:
                self.options.add_argument(option)

    def __enter__(self):
        self.driver = webdriver.Chrome(options=self.options)
        return self.driver

    def __exit__(self, *args, **kwargs):
        if not self.keep_open and self.driver is not None:
            self.driver.quit()
            self.driver = None
