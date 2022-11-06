import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from constants import DEFAULT_URL, DRIVER_VERSION, WEBDRIVERWAIT_TIMEOUT
from locators import LogInLocators


def pytest_addoption(parser):
    parser.addoption("--url", default=DEFAULT_URL)
    parser.addoption("--headless", action="store_true")


@pytest.fixture()
def config(request):
    url = request.config.getoption("--url")
    headless = request.config.getoption("--headless")
    return {"url": url, "headless": headless}


@pytest.fixture(scope="function")
def driver(config):
    url = config["url"]
    headless = config["headless"]
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        options=options,
        service=Service(ChromeDriverManager(version=DRIVER_VERSION).install())
    )
    driver.get(url)
    driver.maximize_window()
    try:
        WebDriverWait(driver, timeout=WEBDRIVERWAIT_TIMEOUT).until(
            EC.element_to_be_clickable(LogInLocators.SIGN_IN_FIRST_LOCATOR))
    except Exception:
        assert False, f"Страница {url} не загрузилась"
    yield driver
    driver.quit()
