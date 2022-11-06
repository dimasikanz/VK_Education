import pytest

from base_case import BaseCase
from locators import BalanceLocators, ElseButtonsLocators, ToolsLocators


@pytest.mark.ui
class TestButtons(BaseCase):
    parametrize_locators = [
        (
            {
                "button_locator_without_else": BalanceLocators.BALANCE_BUTTON_LOCATOR,
                "button_locator_with_else": ElseButtonsLocators.ELSE_BALANCE_BUTTON_LOCATOR,
                "element_for_assert_locator": BalanceLocators.PAYER_LOCATOR
            }
        ),
        (
            {
                "button_locator_without_else": ToolsLocators.TOOLS_BUTTON_LOCATOR,
                "button_locator_with_else": ElseButtonsLocators.ELSE_TOOLS_BUTTON_LOCATOR,
                "element_for_assert_locator": ToolsLocators.FEED_LIST_LOCATOR
            }
        ),
    ]

    @pytest.mark.parametrize("locators", parametrize_locators)
    def test_buttons(self, full_login, locators):
        self.else_and_some_button_click(
            locator_without_else=locators["button_locator_without_else"],
            locator_with_else=locators["button_locator_with_else"]
        )
        self.assert_element_is_displayed_after_page_load(locators["element_for_assert_locator"])
