from datetime import datetime

import allure
import pytest

from base_case import BaseCase


@pytest.mark.ui
class TestCompanies(BaseCase):
    campaign_name = f"DimaCompany{datetime.now().strftime('%y%m%d%H%M%S')}"

    def test_create_campaign_video_views(self, file_path):
        with allure.step("Create new campaign"):
            self.main_page.create_new_campaign(
                campaign_name=self.campaign_name, file_path=file_path
            )
            self.main_page.assert_campaign_is_created(campaign_name=self.campaign_name)
