from datetime import datetime

import pytest
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException,
                                        NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from constants import EMAIL, PASSWORD, SITE_TITLE, WEBDRIVERWAIT_TIMEOUT
from locators import (ElseButtonsLocators, LogInLocators, OtherLocators,
                      ProfileLocators)


class BaseCase:
    driver = None

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver):
        self.driver = driver
        assert SITE_TITLE in self.driver.title, f'Неправильный заголовок сайта: {self.driver.title}'

    def find(self, by, what):
        return self.driver.find_element(by, what)

    def click_button(self, locator):
        button = self.find(*locator)
        button.click()

    def form_send_keys(self, locator, keys):
        form = self.find(*locator)
        form.clear()
        form.send_keys(keys)

    def email_form_send_keys(self, keys):
        """
        Заполнение поля "email" строкой
        """
        email_form = self.find(*LogInLocators.EMAIL_FORM_LOCATOR)
        email_form.clear()
        email_form.send_keys(keys)

    def password_form_send_keys(self, keys):
        """
        Заполнение поля "password" строкой
        """
        password_form = self.find(*LogInLocators.PASSWORD_FORM_LOCATOR)
        password_form.clear()
        password_form.send_keys(keys)

    @pytest.fixture()
    def full_login(self):
        """
        Полная авторизация на сайте
        """
        self.click_button(LogInLocators.SIGN_IN_FIRST_LOCATOR)
        self.email_form_send_keys(EMAIL)
        self.password_form_send_keys(PASSWORD)
        self.click_button(LogInLocators.SIGN_IN_SECOND_LOCATOR)
        # Ждем, пока страница полностью загрузиться (вся верхняя менюшка загружается в первую очередь,
        # поэтому проверяем по центральной части страницы)
        self.wait_for_element_visibility_with_webdriverwait(OtherLocators.PAGE_BACKGROUND_LOCATOR)

    def wait_for_element_visibility_with_webdriverwait(self, locator):
        """
        Ожидание видимости элемента
        """
        try:
            WebDriverWait(self.driver, timeout=WEBDRIVERWAIT_TIMEOUT).until(
                EC.visibility_of_element_located(locator))
        except Exception:
            assert False, f"Element with locator {locator} is not visible"


    def wait_for_element_clickable_with_webdriverwait(self, locator):
        """
        Ожидание кликабельности элемента
        """
        try:
            WebDriverWait(self.driver, timeout=WEBDRIVERWAIT_TIMEOUT).until(
                EC.element_to_be_clickable(locator))
        except Exception:
            assert False, f"Element with locator {locator} is not clickable"


    def click_button_until_clickable(self, locator):
        """
        Метод для повторных кликов по кнопке, в случае, если она оказалась некликабельной,
        либо же вылетела какая-то другая ошибка
        """
        element_is_clickable = False
        start_time = datetime.now()
        time_after_start = 0
        while not element_is_clickable and not time_after_start > 5:
            try:
                self.click_button(locator)
                element_is_clickable = True
            except (
                ElementClickInterceptedException,
                StaleElementReferenceException,
                ElementNotInteractableException,
                NoSuchElementException
            ):
                current_time = datetime.now()
                time_after_start = (current_time - start_time).seconds

    def assert_element_is_displayed_after_page_load(self, locator):
        """
        Проверка, отображен ли элемент на странице, происходит после загрузки страницы
        """
        self.wait_for_element_visibility_with_webdriverwait(locator)
        element = self.find(*locator)
        assert element.is_displayed(), f'Элемент с локатором {locator} не отображен на странице'

    def assert_element_text_after_page_load(self, locator, text_for_assert):
        """
        Проверка, совпадает ли текст элемента на странице с нашим текстом, происходит после загрузки страницы
        (может принимать на вход список)
        """
        self.wait_for_element_visibility_with_webdriverwait(locator)
        element = self.find(*locator)
        assert element.text in text_for_assert, f'Неправильный текст элемента {locator}: "{element.text}"'

    def assert_element_text(self, locator, text_for_assert):
        """
        Проверка, совпадает ли текст элемента на странице с нашим текстом
        (может принимать на вход список)
        """
        element = self.find(*locator)
        assert element.text in text_for_assert, f'Неправильный текст элемента {locator}: "{element.text}"'

    def send_contact_data(self, FIO: str, INN: str, phone: str):
        """
        Заполнение всех полей контактных данных
        """
        self.form_send_keys(ProfileLocators.FIO_FORM_LOCATOR, FIO)
        self.form_send_keys(ProfileLocators.INN_FORM_LOCATOR, INN)
        self.form_send_keys(ProfileLocators.PHONE_FORM_LOCATOR, phone)

    def else_and_some_button_click(self, locator_without_else, locator_with_else):
        """
        Нажатие на кнопку, с учетом того, что она может быть скрыта за кнопкой 'Ещё'
        """
        try:
            self.click_button(locator_without_else)
        except Exception:
            self.click_button(ElseButtonsLocators.ELSE_BUTTON_LOCATOR)
            self.click_button_until_clickable(locator_with_else)
