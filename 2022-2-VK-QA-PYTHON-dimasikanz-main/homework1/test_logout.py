import pytest

from base_case import BaseCase
from locators import AuthorizedUsernameButtonLocators, LogInLocators


@pytest.mark.ui
class TestLogout(BaseCase):
    def test_logout(self, full_login):
        self.click_button(
            AuthorizedUsernameButtonLocators.AUTHORIZED_USER_INFO_BUTTON_LOCATOR
        )
        self.click_button_until_clickable(
            AuthorizedUsernameButtonLocators.LOGOUT_LOCATOR
        )
        self.assert_element_is_displayed_after_page_load(LogInLocators.SIGN_IN_FIRST_LOCATOR)
