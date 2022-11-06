from datetime import datetime

import allure
import pytest

from base_case import BaseCase


@pytest.mark.ui
class TestSegments(BaseCase):
    segment_name_default = f"DimaSegment{datetime.now().strftime('%y%m%d%H%M%S')}"
    segment_name_for_test_with_group = (
        f"VKgroupsegment{datetime.now().strftime('%y%m%d%H%M%S')}"
    )

    def test_create_applications_segment(self):
        with allure.step("Create applications segment"):
            with allure.step("Go to add segment page"):
                segments_page = self.main_page.go_to_the_segments_page()
                segments_page.button_with_possible_different_locators_click(
                    locator_if_zero=segments_page.locators.CREATE_SEGMENT_BUTTON_IF_ZERO_SEGMENTS_LOCATOR,
                    locator_if_not_zero=segments_page.locators.CREATE_SEGMENT_BUTTON_LOCATOR
                )
                with allure.step("Check that we are on the segment creation page"):
                    assert segments_page.find(
                        segments_page.locators.VK_AND_OK_GROUPS_ADD_SEGMENT_BUTTON_LOCATOR
                    ), f"Не найден элемент, соответствующий странице создания кампании: {self.locators.VK_AND_OK_GROUPS_ADD_SEGMENT_BUTTON_LOCATOR}"
            with allure.step("Create application segment"):
                segments_page.applications_and_games_segment_create(
                    segment_name=self.segment_name_default
                )
            segments_page.assert_segment_is_created(
                new_segment_name=self.segment_name_default
            )

    def test_create_and_delete_segment_with_source(self):
        with allure.step("Create and delete segment with source"):
            segments_page = self.main_page.go_to_the_segments_page()
            with allure.step(
                f"Source create url = {segments_page.constants.VK_EDUCATION_GROUP_URL}"
            ):
                segments_page.add_vk_and_ok_groups_source(
                    url=segments_page.constants.VK_EDUCATION_GROUP_URL
                )
                segments_page.assert_element_is_displayed(
                    segments_page.locators.NEW_SOURCE_VK_EDUCATION
                )
            with allure.step("Go to segment create page"):
                segments_page.click(segments_page.locators.SEGMENTS_LIST_BUTTON_LOCATOR)
                segments_page.button_with_possible_different_locators_click(
                    locator_if_zero=segments_page.locators.CREATE_SEGMENT_BUTTON_IF_ZERO_SEGMENTS_LOCATOR,
                    locator_if_not_zero=segments_page.locators.CREATE_SEGMENT_BUTTON_LOCATOR
                )
                with allure.step("Check that we are on the segment creation page"):
                    assert segments_page.find(
                        segments_page.locators.VK_AND_OK_GROUPS_ADD_SEGMENT_BUTTON_LOCATOR
                    ), f"Не найден элемент, соответствующий странице создания кампании: {self.locators.VK_AND_OK_GROUPS_ADD_SEGMENT_BUTTON_LOCATOR}"
            segments_page.vk_education_segment_create(
                self.segment_name_for_test_with_group
            )
            segments_page.assert_segment_is_created(
                new_segment_name=self.segment_name_for_test_with_group
            )
            segments_page.delete_segment(
                segment_name=self.segment_name_for_test_with_group
            )
            segments_page.assert_segment_is_deleted(
                new_segment_name=self.segment_name_for_test_with_group
            )
            segments_page.delete_vk_education_source()
            self.driver.refresh()
            segments_page.assert_text_not_in_page_source(
                segments_page.constants.GROUP_NAME
            )
