import allure
import pytest

from helpers.file_helper import load_file_script


@pytest.fixture()
@allure.title("Полностью очищаю таблицу series")
def truncate_test_data(connect_db):
    def _truncate_data(table_name: str):
        with connect_db.cursor() as cur:
            cur.execute(f"truncate table {table_name}")
        connect_db.commit()
    yield _truncate_data


@pytest.fixture()
@allure.title("Готовлю тестовые данные")
def insert_and_clear_test_data_in_series(connect_db, truncate_test_data):
    with allure.step("Полностью очищаю таблицу series"):
        truncate_test_data("series")
    with allure.step("Вношу тестовые данные в таблицу series"):
        with connect_db.cursor() as cur:
            cur.execute(load_file_script("insert_data_series.sql"))
        connect_db.commit()
    yield
    with allure.step("Полностью очищаю таблицу series"):
        truncate_test_data("series")


@pytest.fixture()
@allure.title("Готовлю тестовые данные")
def insert_string_test_data_in_series(connect_db):
    with allure.step("Вношу тестовые данные в таблицу series"):
        with connect_db.cursor() as cur:
            cur.execute(load_file_script("insert_data_line1_test_series.sql") + "RETURNING id;")
            result_id = cur.fetchone()
        connect_db.commit()

    yield result_id
    with allure.step("Удаляю внесенные данные из таблицы"):
        with connect_db.cursor() as cur:
            cur.execute('''DELETE FROM public.series where id=(%s)
        ''', (result_id['id'],))
        connect_db.commit()


@pytest.fixture()
# request нужен для передачи данных в фикстуру из сессии
@allure.title("Готовлю тестовые данные")
def insert_and_get_count_lines_of_data_in_series(connect_db, truncate_test_data, request):
    if hasattr(request, "param"):
        your_script = request.param
    else:
        your_script = "select_from_series.sql"
    with connect_db.cursor() as cur:
        cur.execute(load_file_script(f"{your_script}"))
        cur.execute(load_file_script("select_from_series.sql"))
        result = cur.fetchall()
    connect_db.commit()
    yield len(result)

    truncate_test_data("series")


@pytest.fixture()
@allure.title("Получаю отсортированные данные по рейтингу на убывание из таблицы БД series")
def sort_data_in_series(connect_db):
    def _sort_data():
        with connect_db.cursor() as cur:
            cur.execute(load_file_script("select_from_series.sql") + " order by rating desc")
            result = cur.fetchall()
        return result

    yield _sort_data


@pytest.fixture()
@allure.title("Получаю данные из таблицы БД series")
def get_data_in_series(connect_db):
    def _get_data():
        with connect_db.cursor() as cur:
            cur.execute(load_file_script("select_from_series.sql"))
            result = cur.fetchall()
        return result

    yield _get_data
