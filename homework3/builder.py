from dataclasses import dataclass
from datetime import datetime


class Builder:
    """
    Датаклассы для составления названий сегментов/кампаний, а также data к запросам
    """

    @staticmethod
    def segment(segment_title=None, data_for_api=None, vk_source=False, object_id=None):
        @dataclass
        class Segment:
            """
            Датакласс для сегментов
            """

            title: str
            data_for_api: dict

        if segment_title is None and not vk_source:
            segment_title = f"DimaSegment{datetime.now().strftime('%y%m%d%H%M%S')}"

        if segment_title is None and vk_source:
            segment_title = f"VKgroupSegment{datetime.now().strftime('%y%m%d%H%M%S')}"

        if data_for_api is None and not vk_source:
            data_for_api = {
                "name": segment_title,
                "pass_condition": 1,
                "relations": [
                    {
                        "object_type": "remarketing_player",
                        "params": {"type": "positive", "left": 365, "right": 0}
                    }
                ]
            }

        if data_for_api is None and vk_source and object_id is not None:
            data_for_api = {
                "name": segment_title,
                "pass_condition": 1,
                "relations": [
                    {
                        "object_type": "remarketing_vk_group",
                        "params": {
                            "source_id": object_id,
                            "type": "positive"
                        }
                    }
                ]
            }
        return Segment(title=segment_title, data_for_api=data_for_api)

    @staticmethod
    def vk_group_source(source_id):
        @dataclass
        class VkSource:
            """
            Датакласс для источника - группы ВК Образование
            """

            data_for_api: dict

        data_for_api = {"items": [{"object_id": source_id}]}

        return VkSource(data_for_api=data_for_api)

    @staticmethod
    def campaign(
        campaign_title=None,
        data_for_api=None,
        uploaded_file_id=None,
        create=None,
        delete=None,
        created_campaign_id=None,
        url_id=None,
        package_id=None
    ):
        @dataclass
        class Campaign:
            """
            Датакласс для кампаний
            Для составления data к api запросам берет различные id, найденные с помощью методов из
            base_case: created_campaign_id - для составления data к api удаления кампании; url_id,
            package_id - для составления data к api запросу создания кампании. Параметры
            create и delete отвечают за то, к чему составлять data - к запросу на создание
            или к запросу на удаление
            """

            campaign_title: str
            data_for_api: dict

        if campaign_title is None:
            campaign_title = f"DimaCampaign{datetime.now().strftime('%y%m%d%H%M%S')}"

        if data_for_api is None and create:
            data_for_api = {
                "name": campaign_title,
                "read_only": False,
                "objective": "videoviews",
                "targetings": {
                    "split_audience": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    "sex": ["male", "female"],
                    "age": {
                        "age_list": [0, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                        "expand": True
                    },
                    "geo": {"regions": []},
                    "interests_soc_dem": [],
                    "segments": [],
                    "interests": [],
                    "fulltime": {
                        "flags": ["use_holidays_moving", "cross_timezone"],
                        "mon": [14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                        "tue": [14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                        "wed": [14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                        "thu": [14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                        "fri": [14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                        "sat": [14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                        "sun": [14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
                    },
                    "pads": [784369, 784370],
                },
                "autobidding_mode": "fixed",
                "uniq_shows_period": "day",
                "mixing": "fastest",
                "enable_utm": True,
                "price": "0.12",
                "max_price": "0",
                "package_id": package_id,
                "banners": [
                    {
                        "urls": {"primary": {"id": url_id}},
                        "content": {"video_landscape_6s": {"id": uploaded_file_id}},
                        "textblocks": {"cta_sites_full": {"text": "visitSite"}},
                        "name": ""
                    }
                ]
            }

        if data_for_api is None and delete and created_campaign_id is not None:
            data_for_api = {"status": "deleted"}
        return Campaign(campaign_title=campaign_title, data_for_api=data_for_api)
