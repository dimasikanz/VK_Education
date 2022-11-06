import allure
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)

import constants
import locators
from base_page import BasePage
from segments_page import SegmentsPage


class MainPage(BasePage):

    locators = locators.MainPageLocators()
    constants = constants.MainPageConstants()

    @allure.step("Go to the segments page")
    def go_to_the_segments_page(self):
        self.click(self.locators.SEGMENTS_BUTTON_LOCATOR)
        return SegmentsPage(self.driver)

    def upload_file(self, locator, file_path):
        with allure.step(f"Upload file from {file_path}"):
            element = self.find(locator)
            element.send_keys(file_path)

    def create_new_campaign(self, campaign_name, file_path):
        with allure.step("Go to create campaign page"):
            self.button_with_possible_different_locators_click(
                locator_if_zero=self.locators.CREATE_CAMPAIGN_BUTTON_LOCATOR_IF_ZERO,
                locator_if_not_zero=self.locators.CREATE_CAMPAIGN_BUTTON_LOCATOR
            )
            self.click(self.locators.VIDEO_VIEWS_PURPOSE_BUTTON_LOCATOR)
        with allure.step("Check that we are on the campaign creation page"):
            assert self.find(
                self.locators.URL_FIELD_LOCATOR
            ), f"Не найден элемент, соответствующий странице создания кампании: {self.locators.URL_FIELD_LOCATOR}"
        with allure.step("Creating new campaign"):
            self.field_send_keys(
                self.locators.URL_FIELD_LOCATOR,
                self.constants.VIDEO_URL
            )
            self.field_send_keys(
                self.locators.CAMPAIGN_NAME_FIELD_LOCATOR, campaign_name
            )
            # Нажатие на кнопку PIN (она открепляет блок со ставкой снизу страницы) необходимо в режиме
            # headless. В нём при переходе на страницу с созданием кампании блок со ставкой
            # перекрывает собой BUMPER_ADS_BUTTON
            self.click(self.locators.PIN_LOCATOR)
            self.click(self.locators.BUMPER_ADS_FORMAT_BUTTON_LOCATOR)
            self.upload_file(self.locators.VIDEO_UPLOAD_BUTTON_LOCATOR, file_path)
            self.assert_element_is_displayed(
                self.locators.UPLOAD_GREEN_CHECK_MARK_LOCATOR
            )
            self.click(self.locators.CREATE_CAMPAIGN_SUBMIT_BUTTON_LOCATOR)
            self.click(self.locators.CAMPAIGNS_BUTTON_LOCATOR)

    def assert_campaign_is_created(self, campaign_name):
        """
        Проверка создания кампании
        В случае, если поле для поиска кампаний не нашелся -
        количество кампаний = 0, т.е. кампания не была создана.
        В случае, если при поиске кампаний не было найдено элементов
        по локатору CAMPAIGNS_IN_SEARCH_LOCATOR - значит была надпись
        "Ничего не найдено", соотвественно кампания не была создана.
        """
        with allure.step(f"Check that campaign '{campaign_name}' is created"):
            try:
                self.field_send_keys(
                    self.locators.CAMPAIGNS_LIST_SEARCH_FIELD_LOCATOR, campaign_name
                )
            except (NoSuchElementException, StaleElementReferenceException):
                assert (
                    False
                ), f"Кампания {campaign_name} не была создана, не было найдено поле для поиска кампаний"
            try:
                first_campaign_in_search = self.find(
                    self.locators.CAMPAIGNS_TEXT_IN_SEARCH_LOCATOR
                )
                assert (
                    first_campaign_in_search.text == campaign_name
                ), f"Кампания {campaign_name} не была создана, элемент из поиска не соответствует созданному"
            except (NoSuchElementException, StaleElementReferenceException):
                assert (
                    False
                ), f"Кампания {campaign_name} не была создана, в поиске по названию пусто"
