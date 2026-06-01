# tests/conftest.py
import os
import csv
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope='function')
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    # Pakai Selenium built-in manager, tidak perlu webdriver-manager
    d = webdriver.Chrome(options=options)
    yield d
    d.quit()

@pytest.fixture(scope='function')
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)

def load_csv(filename: str) -> list:
    filepath = os.path.join('data', filename)
    with open(filepath, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report  = outcome.get_result()
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            os.makedirs('reports/screenshots', exist_ok=True)
            safe_name = (
                item.nodeid
                .replace('/', '_').replace('::', '_')
                .replace('[', '_').replace(']', '')
            )
            path = f'reports/screenshots/{safe_name}.png'
            driver.save_screenshot(path)
            print(f'\nScreenshot disimpan: {path}')