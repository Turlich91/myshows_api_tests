import os

import allure
import pytest


@pytest.fixture()
@allure.title("Получаю список сериалов из API")
def get_series(connect_api_session):
    def _get_series_rq(query_params=""):
        response = connect_api_session.get(os.getenv("BASE_URL") + "/api/v1/series" + query_params)
        assert response.status_code == 200
        return response.json()
    yield _get_series_rq