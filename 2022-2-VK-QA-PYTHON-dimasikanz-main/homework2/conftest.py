import logging

from constants import ConftestConstants
from fixtures import *


def pytest_addoption(parser):
    """
    Парсинг данных из консоли, browser - имя браузера, url - url страницы,
    debug_log - логирование в режиме DEBUG (Если не указано - INFO),
    selenoid - запуск тестов в селеноиде, vnc - запуск тестов в селеноиде
    в режиме vnc, headless - запуск тестов в режиме headless
    """
    parser.addoption("--browser", default="chrome")
    parser.addoption("--url", default="https://target-sandbox.my.com/")
    parser.addoption("--debug_log", action="store_true")
    parser.addoption("--selenoid", action="store_true")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--headless", action="store_true")


@pytest.fixture(scope="session")
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope="session")
def base_temp_dir():
    if sys.platform.startswith("win"):
        base_dir = "C:\\tests"
    else:
        base_dir = "/tmp/tests"
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    return base_dir


@pytest.fixture(scope="function")
def temp_dir(request):
    """
    Создание репозитория для логов и скринов
    """
    test_dir = os.path.join(
        request.config.base_temp_dir,
        request._pyfuncitem.nodeid.replace("/", "_").replace(":", "_")
    )
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope="session")
def config(request):
    browser = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    debug_log = request.config.getoption("--debug_log")
    headless = request.config.getoption("--headless")
    if request.config.getoption("--selenoid"):
        if request.config.getoption("--vnc"):
            vnc = True
        else:
            vnc = False
        selenoid = ConftestConstants.SELENOID
    else:
        selenoid = None
        vnc = False

    return {
        "browser": browser,
        "url": url,
        "debug_log": debug_log,
        "selenoid": selenoid,
        "vnc": vnc,
        "headless": headless
    }


@pytest.fixture(scope="function")
def logger(temp_dir, config):
    """
    Логирование тестов
    """
    log_formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    log_file = os.path.join(temp_dir, "test.log")
    log_level = logging.DEBUG if config["debug_log"] else logging.INFO

    file_handler = logging.FileHandler(log_file, "w")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger("test")
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()
