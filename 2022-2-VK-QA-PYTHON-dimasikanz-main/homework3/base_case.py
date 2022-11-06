import json

import pytest

import constants
from apis import CampaignAPIs, SegmentAPIs, SourceAPIs
from builder import Builder


class ApiBase:
    authorize = True

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, api_client):
        """
        Метод для определения api_client и автоматической авторизации (Получения всех нужных кук)
        Внутри метода реализуется следующая цепочка действий: в первом тесте произойдёт авторизация
        - определение csrftoken и остальных нужных кук, в последующих же тестах, т.к. сессионные
        куки остаются, они будут браться оттуда
        """
        self.api_client = api_client
        self.builder = Builder()

        if self.authorize and self.api_client.session.cookies.get("csrftoken") is None:
            self.api_client.login_with_all_cookies()

    def create_segment(self, data, headers):
        """
        Создание сегмента
        """
        data = json.dumps(data)
        created_segment_id = self.api_client.request_session(
            method="POST",
            location=SegmentAPIs.POST_AND_GET_SEGMENTS_API_LOCATION,
            headers=headers,
            data=data
        )
        created_segment_id = created_segment_id.get("id")
        assert (
            created_segment_id is not None
        ), "Запрос на создание сегмента не вернул id нового сегмента"
        return created_segment_id

    def assert_segment_is_created(self, created_segment_id, segment_name):
        """
        Проверка, был ли сегмент создан
        (Проверка статус кода осуществляется внутри request_session)
        """
        segment_info = self.api_client.request_session(
            method="GET",
            location=f"/api/v2/remarketing/segments/{created_segment_id}.json"
        )
        segment_name_from_request = segment_info["name"]
        assert (
            segment_name_from_request == segment_name
        ), f"Сегмент с именем {segment_name} не был создан, под его id находится {segment_name_from_request}"

    def delete_segment(self, segment_id, headers):
        """
        Удаление сегмента по id
        """
        self.api_client.request_session(
            method="DELETE",
            location=f"/api/v2/remarketing/segments/{segment_id}.json",
            headers=headers,
            expected_status=204,
            jsonify=False
        )

    def assert_segment_is_deleted(self, deleted_segment_id, segment_name):
        """
        Проверка, был ли сегмент удален
        Если по id сегмента ничего не находится - он был удален
        """
        deleted_segment_info = self.api_client.request_session(
            method="GET",
            location=f"/api/v2/remarketing/segments/{deleted_segment_id}.json",
            jsonify=False,
            check_status_code=False
        )
        assert (
            deleted_segment_info.status_code == 404
        ), f"Сегмент {segment_name} не был удален"

    def get_vk_education_group_object_id(self):
        """
        Получение object_id источника - группы ВК Образование
        """
        group_name = constants.VK_EDUCATION_GROUP_TITLE
        params = {"_q": group_name}
        sources_info = self.api_client.request_session(
            method="GET",
            location=SourceAPIs.GET_ALL_VK_GROUPS_SOURCES_LIST_API_LOCATION,
            params=params
        )

        sources = sources_info["items"]
        for source in sources:
            if source["name"] == group_name:
                return source["id"]
        assert False, f"Группа с названием {group_name} не была найдена в источниках"

    def add_group_source(self, data, headers):
        """
        Добавление нового источника данных - группы ОК/ВК, возвращает айди нового
        источника
        """
        data = json.dumps(data)
        info_about_added_vk_education_group = self.api_client.request_session(
            method="POST",
            location=SourceAPIs.POST_NEW_VK_GROUP_SOURCE_API_LOCATION,
            headers=headers,
            data=data,
            expected_status=201
        )
        added_group_source_id = info_about_added_vk_education_group["items"][0]["id"]
        return added_group_source_id

    def delete_group_source(self, headers, source_id_in_my_sources_list):
        """
        Удаление источника данных - группы ОК/ВК по айди
        """
        self.api_client.request_session(
            method="DELETE",
            location=f"/api/v2/remarketing/vk_groups/{source_id_in_my_sources_list}.json",
            headers=headers,
            jsonify=False,
            expected_status=204
        )

    def assert_group_source_is_added(self, added_source_id):
        """
        Проверка, был ли добавлен источник - есть ли добавленный источник в виде группы ОК/ВК в списке
        источников: Группы ОК и ВК
        """
        groups_sources_list = self.api_client.request_session(
            method="GET", location=SourceAPIs.GET_MY_VK_GROUPS_SOURCES_LIST_API_LOCATION
        )
        added_source_is_in_the_list = False
        for source in groups_sources_list["items"]:
            if source["id"] == added_source_id:
                added_source_is_in_the_list = True
                break
        assert (
            added_source_is_in_the_list
        ), f"Источник данных (Группы ОК и ВК) с id {added_source_id} не был добавлен"

    def assert_group_source_is_deleted(self, deleted_source_id):
        """
        Проверка, был ли удален источник - нет ли источника в виде группы ОК/ВК в списке
        источников: Группы ОК и ВК
        """
        groups_sources_list = self.api_client.request_session(
            method="GET", location=SourceAPIs.GET_MY_VK_GROUPS_SOURCES_LIST_API_LOCATION
        )
        source_is_in_the_list = False
        for source in groups_sources_list["items"]:
            if source["id"] == deleted_source_id:
                source_is_in_the_list = True
                break
        assert (
            not source_is_in_the_list
        ), f"Источник данных (Группы ОК и ВК) с id {deleted_source_id} не был удален"

    def upload_file(self, headers, file_path):
        """
        Загрузка видео при создании кампании, возвращает айди загруженного файла
        """
        file = {"file": open(file_path, "rb")}
        uploaded_file_info = self.api_client.request_session(
            method="POST",
            files=file,
            headers=headers,
            location=CampaignAPIs.POST_VIDEO_API_LOCATION
        )
        uploaded_file_id = uploaded_file_info["id"]
        return uploaded_file_id

    def create_campaign(self, data, headers):
        """
        Создание кампании, возвращает айди созданной кампании
        """
        data = json.dumps(data)
        created_campaign_info = self.api_client.request_session(
            method="POST",
            headers=headers,
            data=data,
            location=CampaignAPIs.GET_AND_POST_CAMPAIGN_API_LOCATION
        )
        created_campaign_id = created_campaign_info["id"]
        return created_campaign_id

    def assert_campaign_is_created(self, campaign_id, campaign_title):
        """
        Проверка, что кампания была создана
        (Проверка статус кода осуществляется внутри request_session)
        """
        campaign_info = self.api_client.request_session(
            method="GET",
            location=f"/api/v2/campaigns/{campaign_id}.json"
        )
        campaign_title_from_request = campaign_info["name"]
        assert (
            campaign_title_from_request == campaign_title
        ), f"Кампания {campaign_title} не была создана, под её id находится {campaign_title_from_request}"

    def delete_campaign(self, campaign_id, data, headers):
        """
        Удаление кампании по id
        """
        data = json.dumps(data)
        self.api_client.request_session(
            method="POST",
            expected_status=204,
            data=data,
            headers=headers,
            jsonify=False,
            location=f"/api/v2/campaigns/{campaign_id}.json"
        )

    def assert_campaign_is_deleted(self, campaign_id, campaign_title):
        """
        Проверка, что кампания удалена
        Осуществляется через ручку '/api/v2/campaigns.json', т.к. ручка
        '/api/v2/campaigns/{campaign_id}.json' возвращает даже удалённую кампанию
        """
        campaigns_info = self.api_client.request_session(
            method="GET",
            location=CampaignAPIs.GET_AND_POST_CAMPAIGN_API_LOCATION
        )
        campaign_in_campaign_list = False
        campaigns_list = campaigns_info["items"]
        for campaign in campaigns_list:
            if campaign["id"] == campaign_id:
                campaign_in_campaign_list = True
                break
        assert (
            not campaign_in_campaign_list
        ), f"Кампания {campaign_title} не была удалена"

    def get_url_id(self, url):
        """
        Получение id для видео, ссылку на которое необходимо вставить при создании кампании
        """
        params = {"url": url}
        url_info = self.api_client.request_session(
            method="GET", params=params, location=CampaignAPIs.GET_URL_ID_API_LOCATION
        )
        url_id = url_info["id"]
        return url_id

    def get_package_id(self, package_name):
        """
        Получение package_id по имени package - типу рекламной кампании
        """
        packages_info = self.api_client.request_session(
            method="GET", location=CampaignAPIs.GET_PACKAGE_ID_API_LOCATION
        )
        packages = packages_info["items"]
        for package in packages:
            if package["name"] == package_name:
                package_id = package["id"]
                return package_id
        assert False, f"Нужный package_id ({package_name}) не был найден"
