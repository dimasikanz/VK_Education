import pytest

from base_case import ApiBase


@pytest.mark.API
class TestApiSegments(ApiBase):
    def test_create_and_delete_segment(self):
        """
        Тест на создание и удаление сегмента "Приложения и игры в соцсетях".
        Последовательность: создание сегмента, проверка, что он создан, удаление
        сегмента, проверка, что он удален
        """
        headers = {"X-CSRFToken": f'{self.api_client.session.cookies["csrftoken"]}'}
        segment_title = self.builder.segment().title
        data = self.builder.segment(segment_title=segment_title).data_for_api

        created_segment_id = self.create_segment(data=data, headers=headers)
        self.assert_segment_is_created(
            created_segment_id=created_segment_id,
            segment_name=segment_title
        )

        self.delete_segment(segment_id=created_segment_id, headers=headers)
        self.assert_segment_is_deleted(
            deleted_segment_id=created_segment_id,
            segment_name=segment_title
        )

    def test_create_and_delete_segment_with_source(self):
        """
        Тест на создание источника в виде группы "ВК Образование", создание на его
        основе сегмента, последующее удаление созданного источника и сегмента.
        Последовательность: определение object_id источника - группы ВК Образование,
        добавление этого источника, проверка, что источник добавлен, создание на его
        основе сегмента, проверка, что он создан, удаление созданного сегмента, проверка
        его удаления,удаление созданного источника, проверка его удаления
        """
        headers = {"X-CSRFToken": f"{self.api_client.session.cookies['csrftoken']}"}
        vk_education_group_object_id = self.get_vk_education_group_object_id()
        data = self.builder.vk_group_source(vk_education_group_object_id).data_for_api

        added_group_source_id_in_my_sources_list = self.add_group_source(
            data=data, headers=headers
        )
        self.assert_group_source_is_added(
            added_source_id=added_group_source_id_in_my_sources_list
        )

        segment_title = self.builder.segment(vk_source=True).title
        data = self.builder.segment(
            segment_title=segment_title,
            vk_source=True,
            object_id=vk_education_group_object_id
        ).data_for_api

        created_segment_id = self.create_segment(data=data, headers=headers)
        self.assert_segment_is_created(
            created_segment_id=created_segment_id,
            segment_name=segment_title
        )

        self.delete_segment(segment_id=created_segment_id, headers=headers)
        self.assert_segment_is_deleted(
            deleted_segment_id=created_segment_id,
            segment_name=segment_title
        )

        self.delete_group_source(
            headers=headers,
            source_id_in_my_sources_list=added_group_source_id_in_my_sources_list
        )
        self.assert_group_source_is_deleted(
            deleted_source_id=added_group_source_id_in_my_sources_list
        )
