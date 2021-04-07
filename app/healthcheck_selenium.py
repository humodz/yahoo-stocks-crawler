"""
Use this to test if selenium, chrome and chromedriver are working properly
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver = None

try:
    print('starting...')
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    # driver.get('https://example.org')
    driver.get('https://finance.yahoo.com/screener/new')

    print('=' * 10, 'title', '=' * 9)
    print(driver.title)

    body = driver.find_element_by_css_selector('body')
    body_text = body.get_property('innerText')
    print('=' * 10, 'body', '=' * 10)
    print(body_text)
finally:
    if driver:
        driver.quit()
