import constants
from apiclient import ApiClient
from fixtures import *


def pytest_addoption(parser):
    parser.addoption("--url", default=constants.DEFAULT_URL)


@pytest.fixture(scope="session")
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope="session")
def config(request):
    url = request.config.getoption("--url")

    return {
        "url": url
    }


@pytest.fixture(scope="session")
def api_client(config):
    """
    Возврат класса ApiClient
    """
    return ApiClient(
        base_url=config["url"],
        login=constants.AUTHORIZE_DATA[0],
        password=constants.AUTHORIZE_DATA[1]
    )
