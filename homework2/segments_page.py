import allure
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)

import constants
import locators
from base_page import BasePage


class SegmentsPage(BasePage):

    locators = locators.SegmentsPageLocators()
    constants = constants.SegmentsPageConstants()
    url = constants.SEGMENTS_PAGE_URL

    def assert_segment_is_deleted(self, new_segment_name):
        """
        Проверка удаления сегмента
        В случае, если поле для поиска сегментов не нашлось - количество сегментов = 0, значит,
        сегмент был удален и можно делать return (успешную проверку)
        Если ни один элемент не найдётся в поиске, то в first_segment_in_search.text попадёт
        "Ничего не найдено", это не помешает assert`у
        """
        with allure.step(f"Assert: segment with name '{new_segment_name}' is deleted"):
            try:
                self.field_send_keys(
                    self.locators.SEGMENTS_LIST_SEARCH_FIELD_LOCATOR, new_segment_name
                )
            except (NoSuchElementException, StaleElementReferenceException):
                return
            first_segment_in_search = self.find(
                self.locators.SEGMENTS_IN_SEARCH_LOCATOR
            )
            assert (
                first_segment_in_search.text != new_segment_name
            ), f"Сегмент {new_segment_name} не был удалён"

    def assert_segment_is_created(self, new_segment_name):
        """
        Проверка создания сегмента
        """
        with allure.step(f"Check what segment {new_segment_name} is created"):
            self.field_send_keys(
                self.locators.SEGMENTS_LIST_SEARCH_FIELD_LOCATOR, new_segment_name
            )
            first_segment_in_search = self.find(
                self.locators.SEGMENTS_IN_SEARCH_LOCATOR
            )
            assert (
                first_segment_in_search.text == new_segment_name
            ), f"Сегмент {new_segment_name} не был создан"

    def add_vk_and_ok_groups_source(self, url):
        """
        Добавление нового источника 'Группы ОК и ВК', можно указать url источника
        """
        with allure.step(f"Add source with url {url}"):
            self.click(self.locators.VK_AND_OK_GROUPS_SOURCE_BUTTON_LOCATOR)
            self.field_send_keys(self.locators.GROUP_URL_FIELD_LOCATOR, url)
            self.click(self.locators.SELECT_ALL_LOCATOR)
            self.click(self.locators.ADD_SELECTED_ITEMS_BUTTON_LOCATOR)

    def vk_education_segment_create(self, segment_name):
        """
        Создание сегмента 'Группы ОК и ВК' с источником в виде группы ВК 'VK Образование'
        """
        with allure.step(f"Create segment with name '{segment_name}'"):
            self.click(self.locators.VK_AND_OK_GROUPS_ADD_SEGMENT_BUTTON_LOCATOR)
            self.click(self.locators.CHECKBOX_DURING_ADD_SEGMENT_LOCATOR)
            self.click(self.locators.ADD_SEGMENT_BUTTON_LOCATOR)
            self.field_send_keys(self.locators.SEGMENT_NAME_FIELD_LOCATOR, segment_name)
            self.click(self.locators.FINAL_CREATE_SEGMENT_BUTTON_LOCATOR)

    def applications_and_games_segment_create(self, segment_name):
        """
        Создание сегмента 'Приложения и игры в соцсетях'
        """
        with allure.step(
            f"Create applications and games segment with name '{segment_name}'"
        ):
            self.click(self.locators.APPLICATIONS_AND_GAMES_ADD_SEGMENT_BUTTON_LOCATOR)
            self.click(self.locators.CHECKBOX_DURING_ADD_SEGMENT_LOCATOR)
            self.click(self.locators.ADD_SEGMENT_BUTTON_LOCATOR)
            self.field_send_keys(self.locators.SEGMENT_NAME_FIELD_LOCATOR, segment_name)
            self.click(self.locators.FINAL_CREATE_SEGMENT_BUTTON_LOCATOR)

    @allure.step("Delete last added segment")
    def delete_segment(self, segment_name):
        """
        Удаление сегмента по имени
        """
        self.field_send_keys(
            self.locators.SEGMENTS_LIST_SEARCH_FIELD_LOCATOR, segment_name
        )
        first_segment_in_search = self.find(self.locators.SEGMENTS_IN_SEARCH_LOCATOR)
        self.click(first_segment_in_search)
        self.click(self.locators.NEW_SEGMENT_CHECKBOX_LOCATOR)
        self.click(self.locators.SELECT_ACTION_WITH_SEGMENT_BUTTON_LOCATOR)
        self.click(self.locators.DELETE_SEGMENT_BUTTON)

    @allure.step("Delete source 'VK Education'")
    def delete_vk_education_source(self):
        """
        Удаление источника: группа ВК 'ВК Образование'
        """
        self.click(self.locators.VK_AND_OK_GROUPS_SOURCE_BUTTON_LOCATOR)
        self.click(self.locators.DELETE_SOURCE_VK_EDUCATION)
        self.click(self.locators.CONFIRM_REMOVE_BUTTON_LOCATOR)
