import time

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import constants
import locators
from constants import WaitConstants


class PageNotOpenedExeption(Exception):
    pass


class BasePage(object):
    locators = locators.BasePage()
    constants = constants.BasePageConstants()
    url = constants.BASE_PAGE_URL

    def is_opened(self, timeout=WaitConstants.IS_OPENED_TIMEOUT_DEFAULT):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.driver.current_url == self.url:
                return True
        raise PageNotOpenedExeption(
            f"{self.url} did not open in {timeout} sec, current url {self.driver.current_url}"
        )

    def __init__(self, driver):
        self.driver = driver
        self.is_opened()

    def wait(self, timeout=None):
        if timeout is None:
            timeout = WaitConstants.WEB_DRIVER_WAIT_DEFAULT_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=None):
        with allure.step(f"Click element with locator = {locator}"):
            elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
            elem.click()

    def button_with_possible_different_locators_click(
        self, locator_if_zero, locator_if_not_zero
    ):
        """
        Метод для клика по кнопке, которая может быть в разных местах.
        В нашем случае метод работает для создания новой кампании и нового сегмента, т.к.
        если ни одного сегмента/кампании у пользователя нет, то кнопка будет совершенно другой
        """
        try:
            self.click(locator_if_not_zero, timeout=5)
        except (Exception):
            self.click(locator_if_zero, timeout=5)

    @allure.step("Assert: element is visible")
    def assert_element_is_displayed(self, locator, timeout=None):
        with allure.step(f"Check that element with locator {locator} is displayed"):
            try:
                self.wait(timeout).until(EC.visibility_of_element_located(locator))
            except TimeoutException:
                assert False, f"Элемента с локатором {locator} нет на странице"

    @allure.step("Assert: text not in page source")
    def assert_text_not_in_page_source(self, text):
        with allure.step(f"Check that text='{text}' not displayed"):
            assert (
                text not in self.driver.page_source
            ), f"Текст '{text}' присутствует на странице, хотя его не должно быть"

    @allure.step("Send keys in the field")
    def field_send_keys(self, locator, keys):
        with allure.step(f"Send {keys} in the field with locator = {locator}"):
            field = self.wait().until(EC.element_to_be_clickable(locator))
            field.clear()
            field.send_keys(keys)
