import os

import allure
import psycopg
import pytest
import requests
from psycopg.rows import dict_row


from helpers.api_helper import ApiSession


@pytest.fixture(scope="session")
@allure.title("Устанавливаю соединение с API сессией")
def connect_api_session():
    with requests.Session() as api_session:
        yield ApiSession(api_session)

@allure.title("Устанавливаю соединение с БД")
@pytest.fixture(scope="session")
def connect_db():
    with psycopg.connect(os.getenv("DB_CONNECT_CONFIG"), row_factory=dict_row) as conn:
        yield conn