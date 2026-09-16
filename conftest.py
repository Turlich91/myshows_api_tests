import subprocess
import pytest

from dotenv import load_dotenv

pytest_plugins = ["fixtures.connection_fixtures", "fixtures.db_data_fixtures"]


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--html-report",
        action="store_true",
        default=False,
        help="Сгенерировать отчет в формате HTML в директорию allure-report"
    )


def pytest_sessionfinish(session):
    if session.config.getoption("--html-report"):
        subprocess.call(["allure", "generate", "--clean", "--single-file", "allure-results"])
