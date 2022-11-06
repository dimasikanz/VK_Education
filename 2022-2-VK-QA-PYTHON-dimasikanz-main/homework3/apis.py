class SegmentAPIs:
    POST_AND_GET_SEGMENTS_API_LOCATION = "/api/v2/remarketing/segments.json"


class CampaignAPIs:
    GET_AND_POST_CAMPAIGN_API_LOCATION = "/api/v2/campaigns.json"
    POST_VIDEO_API_LOCATION = "/api/v2/content/video.json"
    GET_URL_ID_API_LOCATION = "/api/v1/urls/"
    GET_PACKAGE_ID_API_LOCATION = "/api/v2/packages.json"


class SourceAPIs:
    GET_ALL_VK_GROUPS_SOURCES_LIST_API_LOCATION = "/api/v2/vk_groups.json"
    POST_NEW_VK_GROUP_SOURCE_API_LOCATION = "/api/v2/remarketing/vk_groups/bulk.json"
    GET_MY_VK_GROUPS_SOURCES_LIST_API_LOCATION = "/api/v2/remarketing/vk_groups.json"


class LoginAPIs:
    POST_TAKE_SSDC_MRCU_MC_COOKIES_API_URL = "https://auth-ac.my.com/auth"
    GET_SDC_COOKIE_API_LOCATION = "/sdc"
    GET_CSRFTOKEN_API_LOCATION = "/csrf/"
