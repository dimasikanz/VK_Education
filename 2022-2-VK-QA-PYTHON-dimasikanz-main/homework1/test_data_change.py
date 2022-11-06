from random import randint

import pytest
from faker import Faker

from base_case import BaseCase
from constants import FAKER_LOCALE
from locators import (AuthorizedUsernameButtonLocators, ElseButtonsLocators,
                      ProfileLocators)

fake_ru_data = Faker(FAKER_LOCALE)
data_for_change = {
    "full_name": fake_ru_data.name(),
    "inn": fake_ru_data.individuals_inn(),
    "phone": f"+7{str(randint(1000000000, 9999999999))}"
}


@pytest.mark.ui
class TestDataChange(BaseCase):
    def test_data_change(self, full_login):
        self.else_and_some_button_click(
            locator_without_else=ProfileLocators.PROFILE_BUTTON_LOCATOR,
            locator_with_else=ElseButtonsLocators.ELSE_PROFILE_BUTTON_LOCATOR
        )
        self.assert_element_is_displayed_after_page_load(
            ProfileLocators.CONTACT_INFORMATION_TITLE_LOCATOR
        )
        self.send_contact_data(
            data_for_change["full_name"],
            data_for_change["inn"],
            data_for_change["phone"]
        )
        self.click_button(ProfileLocators.SAVE_BUTTON_LOCATOR)
        self.wait_for_element_visibility_with_webdriverwait(ProfileLocators.SUCCESS_NOTIFICATION_LOCATOR)
        self.driver.refresh()
        self.assert_element_text_after_page_load(
            AuthorizedUsernameButtonLocators.AUTHORIZED_USERNAME_LOCATOR,
            text_for_assert=data_for_change["full_name"].upper()
        )
