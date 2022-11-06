import os
import shutil
import sys

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from base_page import BasePage
from constants import FixturesConstants
from login_page import LoginPage
from main_page import MainPage
from segments_page import SegmentsPage


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture
def segment_page(driver):
    return SegmentsPage(driver=driver)


@pytest.fixture()
def driver(config, temp_dir):
    browser = config["browser"]
    url = config["url"]
    selenoid = config["selenoid"]
    vnc = config["vnc"]
    headless = config["headless"]
    options = add_options(headless=headless, temp_dir=temp_dir)
    driver = get_driver(
        browser_name=browser, url=url, selenoid=selenoid, vnc=vnc, options=options
    )
    yield driver
    with allure.step("Close browser"):
        driver.quit()


@allure.step("Open browser")
def get_driver(
    browser_name,
    url,
    selenoid=None,
    vnc=None,
    options=None,
    headless=None,
    temp_dir=None
):
    """
    Получение driver с нужными настройками и версией драйвера
    """
    if options is None:
        options = add_options(headless, temp_dir)
    if selenoid is not None and selenoid:
        capabilities = {"selenoid:options": {"enableVNC": False, "enableVideo": False}}
        if vnc:
            capabilities["enableVNC"] = True
        options.set_capability("selenoid:options", capabilities)
        driver = webdriver.Remote(command_executor=selenoid, options=options)
    else:
        if browser_name == "chrome":
            driver = webdriver.Chrome(
                options=options,
                service=Service(
                    ChromeDriverManager(
                        version=FixturesConstants.DRIVER_VERSION
                    ).install()
                )
            )
        else:
            raise RuntimeError(f'Unsupported browser: "{browser_name}"')
    driver.get(url)
    driver.maximize_window()
    return driver


def add_options(headless, temp_dir=None):
    """
    Выставление всех настроек драйвера
    """
    with allure.step("Add options for driver"):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if temp_dir is not None:
            options.add_experimental_option(
                "prefs", {"download.default_directory": temp_dir}
            )
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
        return options


@pytest.fixture(scope="session")
def cookies(config):
    """
    Получение куки после авторизации (для последующих входов уже через куки)
    """
    with allure.step("Getting cookies"):
        browser = config["browser"]
        selenoid = config["selenoid"]
        vnc = config["vnc"]
        headless = config["headless"]
        url = config["url"]
        driver = get_driver(
            browser_name=browser, url=url, selenoid=selenoid, vnc=vnc, headless=headless
        )
        login_page = LoginPage(driver)
        login_page.login(*FixturesConstants.AUTHORIZE_DATA)
        cookies = driver.get_cookies()
        with allure.step("Close 'cookies' browser "):
            driver.quit()
        return cookies


def pytest_configure(config):
    """
    Определение пути к файлу для логов и скринов в зависимости от системы, а также
    удаление этого файла в случае, если он уже есть
    """
    if sys.platform.startswith("win"):
        base_dir = FixturesConstants.BASE_DIR_WIN
    else:
        base_dir = FixturesConstants.BASE_DIR_LIN
    if not hasattr(config, "workerunput"):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@pytest.fixture()
def file_path(repo_root):
    """
    Определение пути к файлу, предназначенномиу для загрузки
    """
    return os.path.join(repo_root, FixturesConstants.UPLOAD_FILE_NAME)
