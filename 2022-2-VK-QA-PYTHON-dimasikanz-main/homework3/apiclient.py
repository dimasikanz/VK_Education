from urllib.parse import urljoin

import requests

import constants
from apis import LoginAPIs


class JSONErrorException(Exception):
    pass


class ApiClient:
    def __init__(self, base_url: str, login: str, password: str):
        self.base_url = base_url
        self.login = login
        self.password = password
        self.session = requests.Session()

    def login_with_all_cookies(self):
        """
        Метод для получения в сессию кук, нужных для авторизированных запросов.
        Необходимые куки: csrftoken, mc и sdc. Для получения csrftoken через api
        https://target-sandbox.my.com/csrf/ Нужны: mc, sdc, mrcu куки
        Сначала в https://auth-ac.my.com/auth передаем email и password, получаем mc,ssdc и mrcu куки
        C этими куками в сессии идём на https://target-sandbox.my.com/sdc и получаем sdc куку, с
        которой уже можно сделать запрос на https://target-sandbox.my.com/csrf/ и получить csrf токен
        """
        self.__set_mc_mrcu_ssdc_cookies_in_session()
        self.__set_sdc_cookie_in_session()
        self.__set_csrftoken_in_session()

    def __set_mc_mrcu_ssdc_cookies_in_session(self):
        """
        Получение в сессию кук mc, mrcu, ssdc через запрос на https://auth-ac.my.com/auth с
        логином и паролем в data, также в заголовках указывается Referer
        """
        data = {
            "email": self.login,
            "password": self.password
        }
        headers = {"Referer": constants.DEFAULT_URL}
        self.request_session(
            method="POST",
            location=LoginAPIs.POST_TAKE_SSDC_MRCU_MC_COOKIES_API_URL,
            headers=headers,
            data=data,
            expected_status=302,
            base_url_join=False,
            jsonify=False
        )

    def __set_sdc_cookie_in_session(self):
        """
        Получение в сессию куки sdc
        Запрос на https://target-sandbox.my.com/sdc (mc и mrcu куки находятся в сессии)
        """
        self.request_session(
            method="GET",
            location=LoginAPIs.GET_SDC_COOKIE_API_LOCATION,
            expected_status=302,
            jsonify=False
        )

    def __set_csrftoken_in_session(self):
        """
        Получение в сессию csrf токена
        Запрос на https://target-sandbox.my.com/csrf/ (mc, mrcu, sdc куки находятся в сессии)
        """
        self.request_session(
            method="GET",
            location=LoginAPIs.GET_CSRFTOKEN_API_LOCATION,
            expected_status=200,
            allow_redirects=True,
            jsonify=False
        )

    def request_session(
        self,
        method,
        location,
        headers=None,
        data=None,
        params=None,
        allow_redirects=False,
        expected_status=200,
        jsonify=True,
        base_url_join=True,
        files=None,
        check_status_code=True
    ):
        """
        Сессионный запрос
        jsonify - перевод ответа в json, в случае, если True - метод возвращает словарь,
        если False - возвращает ответ на запрос
        base_url_join - переменная, отвечающая за выбор: соединять location с базовым url или использовать
        в качестве url строку, переданную в location
        """
        if base_url_join is True:
            url = urljoin(self.base_url, location)
        else:
            url = location
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params,
            allow_redirects=allow_redirects,
            files=files
        )

        if check_status_code:
            assert (
                response.status_code == expected_status
            ), f"Expected {expected_status}, but got {response.status_code}"

        if jsonify:
            try:
                json_response: dict = response.json()
            except JSONErrorException:
                raise JSONErrorException(
                    f"Expected json response from api request {url}"
                )
            return json_response
        return response
