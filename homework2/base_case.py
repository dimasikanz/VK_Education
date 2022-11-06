import os

import allure
import pytest
from _pytest.fixtures import FixtureRequest

from login_page import LoginPage
from main_page import MainPage


class BaseCase:
    driver = None
    authorize = True

    @pytest.fixture(scope="function", autouse=True)
    def ui_report(self, driver, request, temp_dir):
        """
        Запись браузерных логов, скринов
        Отправка логов (в том числе и тестовых), скринов в allure
        """
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(temp_dir, "browser.log")
            with open(browser_logs, "w") as f:
                for i in driver.get_log("browser"):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            screenshot_path = os.path.join(temp_dir, "failed.png")
            self.driver.save_screenshot(filename=screenshot_path)
            allure.attach.file(
                screenshot_path, "failed.png", allure.attachment_type.PNG
            )
            with open(browser_logs, "r") as f:
                allure.attach(f.read(), "test.log", allure.attachment_type.TEXT)

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.login_page: LoginPage = request.getfixturevalue("login_page")
        if self.authorize:
            cookies = request.getfixturevalue("cookies")
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.main_page: MainPage = request.getfixturevalue("main_page")
