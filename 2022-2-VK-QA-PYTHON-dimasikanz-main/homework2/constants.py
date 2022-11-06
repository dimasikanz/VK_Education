class BasePageConstants:
    BASE_PAGE_URL = "https://target-sandbox.my.com/dashboard"


class WaitConstants:
    WEB_DRIVER_WAIT_DEFAULT_TIMEOUT = 10
    IS_OPENED_TIMEOUT_DEFAULT = 15


class LoginPageConstants:
    LOGIN_PAGE_URL = "https://target-sandbox.my.com/"


class FixturesConstants:
    DEFAULT_URL = "https://target-sandbox.my.com/"
    DRIVER_VERSION = "105.0.5195.19"
    AUTHORIZE_DATA = ["dimasikanz_2012@mail.ru", "12345q"]
    UPLOAD_FILE_NAME = "video_6sec.mp4"
    BASE_DIR_WIN = "C:/tests"
    BASE_DIR_LIN = "/tmp/tests"


class ConftestConstants:
    SELENOID = "http://127.0.0.1:4444/wd/hub"


class MainPageConstants:
    VIDEO_URL = "https://www.youtube.com/watch?v=Qe-kDHq-Vw4"


class SegmentsPageConstants:
    SEGMENTS_PAGE_URL = "https://target-sandbox.my.com/segments/segments_list"
    GROUP_NAME = "VK Образование"
    VK_EDUCATION_GROUP_URL = "https://vk.com/vkedu"
