import allure

import constants
from base_page import BasePage
from locators import LoginPageLocators
from main_page import MainPage


class LoginPage(BasePage):

    locators = LoginPageLocators
    constants = constants.LoginPageConstants()
    url = constants.LOGIN_PAGE_URL

    def login(self, user, password):
        with allure.step(f"Log in with user = {user}, password = {password}"):
            self.click(self.locators.SIGN_IN_FIRST_LOCATOR)
            self.find(self.locators.EMAIL_FORM_LOCATOR).send_keys(user)
            self.find(self.locators.PASSWORD_FORM_LOCATOR).send_keys(password)
            self.click(self.locators.SIGN_IN_SECOND_LOCATOR)
            return MainPage(self.driver)
