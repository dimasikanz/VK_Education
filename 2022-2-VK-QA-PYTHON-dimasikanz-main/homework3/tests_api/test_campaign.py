import pytest

import constants
from base_case import ApiBase


@pytest.mark.API
class TestApiCampaign(ApiBase):
    def test_create_and_delete_campaign(self, file_path):
        """
        Тест на создание и удаление кампании 'Просмотр видео'.
        Последовательность: загрузка 6-секундного видео на сервер c получением
        его айди, получение айди для ссылки на рекламируемое видео, получение package_id для
        данного типа рекламной кампании, создание кампании 'Просмотр видео' на основе этих
        айдишников, проверка, что кампания создана, удаление созданной кампании, проверка её
        удаления
        """
        headers = {"X-CSRFToken": f"{self.api_client.session.cookies['csrftoken']}"}
        uploaded_file_id = self.upload_file(headers=headers, file_path=file_path)
        url_id = self.get_url_id(url=constants.VIDEO_FOR_CAMPAIGN_URL)
        package_id = self.get_package_id(
            package_name=constants.PACKAGE_NAME_FOR_CREATE_VIEW_VIDEO_CAMPAIGN
        )

        campaign_title = self.builder.campaign().campaign_title
        data = self.builder.campaign(
            campaign_title=campaign_title,
            create=True,
            uploaded_file_id=uploaded_file_id,
            url_id=url_id,
            package_id=package_id
        ).data_for_api

        created_campaign_id = self.create_campaign(data=data, headers=headers)
        self.assert_campaign_is_created(
            campaign_id=created_campaign_id, campaign_title=campaign_title
        )

        data = self.builder.campaign(
            created_campaign_id=created_campaign_id, delete=True
        ).data_for_api

        self.delete_campaign(
            campaign_id=created_campaign_id, data=data, headers=headers
        )
        self.assert_campaign_is_deleted(
            campaign_id=created_campaign_id, campaign_title=campaign_title
        )
