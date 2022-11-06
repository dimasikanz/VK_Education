import pytest

from base_case import BaseCase
from constants import (EMAIL, INVALID_LOGIN_INFO_TEXT, LIMIT_EXCEEDED_TEXT,
                       LOGIN_TEXT_DICT, PASSWORD)
from locators import AuthorizedUsernameButtonLocators, LogInLocators


@pytest.mark.ui
class TestLogin(BaseCase):
    def test_login(self, full_login):
        assert (
            LOGIN_TEXT_DICT["ru"] not in self.driver.page_source
            and LOGIN_TEXT_DICT["ru"] not in self.driver.page_source
        )
        self.assert_element_is_displayed_after_page_load(AuthorizedUsernameButtonLocators.AUTHORIZED_USERNAME_LOCATOR)

    def test_negative_authorization_wrong_password(self):
        self.click_button(LogInLocators.SIGN_IN_FIRST_LOCATOR)
        self.email_form_send_keys(EMAIL)
        self.password_form_send_keys(PASSWORD + "wrong")
        self.click_button(LogInLocators.SIGN_IN_SECOND_LOCATOR)
        self.assert_element_text_after_page_load(
            LogInLocators.AUTHORIZATION_ERROR_LOCATOR,
            text_for_assert=(INVALID_LOGIN_INFO_TEXT,
                             LIMIT_EXCEEDED_TEXT)
        )

    def test_negative_authorization_wrong_email(self):
        self.click_button(LogInLocators.SIGN_IN_FIRST_LOCATOR)
        self.email_form_send_keys(EMAIL + "wrong")
        self.password_form_send_keys(PASSWORD)
        self.click_button(LogInLocators.SIGN_IN_SECOND_LOCATOR)
        self.assert_element_text_after_page_load(
            LogInLocators.AUTHORIZATION_ERROR_LOCATOR,
            text_for_assert=(INVALID_LOGIN_INFO_TEXT,
                             LIMIT_EXCEEDED_TEXT)
        )

    def test_negative_authorization_empty_password(self):
        self.click_button(LogInLocators.SIGN_IN_FIRST_LOCATOR)
        self.email_form_send_keys(EMAIL)
        self.click_button(LogInLocators.SIGN_IN_SECOND_LOCATOR)
        self.click_button(LogInLocators.SIGN_IN_SECOND_LOCATOR)
        self.assert_element_text(
            LogInLocators.SIGN_IN_FIRST_LOCATOR,
            text_for_assert=(LOGIN_TEXT_DICT["ru"],
                             LOGIN_TEXT_DICT["en"])
        )
