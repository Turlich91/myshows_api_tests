# 🎬 myshows_api_tests

Учебный проект по автоматизации **API-тестирования** сервиса **My Shows Rating** — небольшого бэкенда
для ведения личного списка сериалов (название, постер, оценка, статус просмотра и отзыв).

⚠️ВНИМАНИЕ: Проверки написаны по заданиям в ходе учебного процесса. Некоторые тесты реализованы для отработки 
специальных навыков. Это не выбранные мною обязательные Smoke тесты. Каких то проверок может не хватать, но 
периодически я буду дополнять проект. Цель проекта показать навыки AQA которыми я владею

Тесты написаны на **Python + pytest**, проверяют REST API, сверяют ответы напрямую
с данными в **PostgreSQL** и формируют отчёт в **Allure**.
Всё окружение (база, бэкенд и раннер тестов) поднимается одной командой в **Docker Compose**.

---

## 🧰 Стек

| Инструмент | Зачем нужен |
|---|---|
| `pytest` | запуск и параметризация тестов |
| `requests` | HTTP-клиент, обёрнут в свой `ApiSession` |
| `psycopg` (v3) | подключение к PostgreSQL, строки отдаются как `dict` |
| `jsonschema` + `PyYAML` | валидация ответов API по схемам из `schemas/` |
| `allure-pytest` | шаги, вложения с запросом/ответом, HTML-отчёт |
| `pytest-check` | мягкие проверки (`--check-max-tb=100`) |
| `python-dotenv` | переменные окружения из `.env` |
| `Docker Compose` | БД + бэкенд + тесты в одной сети |

---

## 🧪 Что покрыто тестами

### `GET /api/v1/series` — класс `TestGetSeries`

| Тест | Идея проверки |
|---|---|
| `test__get_series_scheme` | ответ не пустой и соответствует JSON-схеме `get_series.yml` |
| `test__get_series_sort_rating_desc` | сортировка `?sort=rating_desc` совпадает с выборкой из БД `order by rating desc` |
| `test__get_series_content` | данные в ответе API идентичны данным в таблице `series` |
| `test__get_lines_of_data_in_series` | параметризация: 3 строки / 1 строка / пустая выборка — схема валидна, количество строк в БД = количеству объектов в ответе |
| `test__get_series_validation_rating_error` | негативный: невалидный `?status=custom_status` → `400` |

### `PUT /api/v1/series/{id}` — класс `TestPutSeries`

`test__put_series_parameters` параметризован пятью наборами из `data/put_data_series.py`
(`change_name`, `change_photo`, `change_rating`, `change_status`, `change_review`):
подменяем по одному полю, проверяем статус `200`, а затем сверяем результат
и с ответом `GET`, и с содержимым базы, и с исходным макетом данных.

### 🐞 Найденные баги

- `test__get_series_content` помечен `@pytest.mark.xfail` — **API отдаёт только 5 записей**,
  хотя в таблице их больше. По этой же причине в тесте сортировки сравнение идёт по срезу `db_data[:5]`
  (сама сортировка при этом работает корректно).

### 🏷 Маркеры

```bash
pytest -m positive     # позитивные сценарии
pytest -m negative     # негативные сценарии
```

---

## 🗂 Структура проекта

```
myshows_api_tests/
├── test_myshows_api.py   # сами тесты: TestGetSeries и TestPutSeries
├── conftest.py           # подключение фикстур, .env, опция --html-report
├── pytest.ini            # allure-dir, маркеры, настройки pytest-check
├── fixtures/
│   ├── connection_fixtures.py  # сессия requests (ApiSession) и коннект к PostgreSQL
│   ├── api_fixtures.py         # get_series — запрос списка сериалов к API
│   └── db_data_fixtures.py     # подготовка/очистка тестовых данных в таблице series
├── helpers/
│   ├── api_helper.py           # обёртка над requests.Session с Allure-вложениями
│   └── file_helper.py          # загрузка YAML-схем и SQL-скриптов
├── schemas/
│   └── get_series.yml          # JSON-схема ответа GET /api/v1/series
├── data/
│   ├── insert_data_series.sql              # набор тестовых данных (много строк)
│   ├── insert_data_lines3_test_series.sql  # набор из 3 строк
│   ├── insert_data_line1_test_series.sql   # одна строка ("Сопрано")
│   ├── select_from_series.sql              # SELECT * FROM SERIES
│   └── put_data_series.py                  # макеты тел запроса для PUT
├── docker-compose.yml    # msr-db + msr-backend + api-tests
└── Dockerfile            # образ раннера тестов (python:3.12-slim)
```

**Как устроены данные:** каждый тест сам готовит себе базу — фикстуры
`truncate_test_data`, `insert_and_clear_test_data_in_series`, `insert_string_test_data_in_series`
чистят таблицу `series`, заливают нужный SQL-скрипт и после теста убирают за собой.
Благодаря этому тесты не зависят друг от друга и от порядка запуска.

---

## ⚙️ Переменные окружения

В корне проекта нужен файл `.env` (в git не коммитится):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456
POSTGRES_DB=my-shows-rating
PORT=80

BASE_URL=http://localhost:80
DB_CONNECT_CONFIG=postgresql://postgres:123456@127.0.0.1:5432/my-shows-rating
```

> При запуске через `docker compose` сервис `api-tests` получает свои `BASE_URL`
> и `DB_CONNECT_CONFIG` из `docker-compose.yml` (адреса внутри сети: `msr-backend`, `msr-db`).
> Значения выше нужны для запуска тестов **локально**, с хоста.

---

## 🚀 Быстрый старт

```bash
docker compose up -d --build      # поднять БД, бэкенд и прогнать тесты
docker compose logs api-tests     # посмотреть результат прогона
allure serve allure-results/      # открыть отчёт
```

Локальный запуск (когда контейнеры с БД и бэкендом уже подняты):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -v
pytest -v --html-report           # дополнительно соберёт allure-report одним файлом
```

---

# Основные моменты проекта myshows_api_tests

Не забудь после окончания работы ввести команду `docker compose down`, 
чтобы остановить и удалить все контейнеры.

А если захочешь в дальнейшем вернуться к тестированию этого сервиса, то снова открой 
в терминале папку с проектом и внутри нее выполни команду `docker compose up -d`

Подключиться к базе данных можно через [Dbeaver](https://dbeaver.io/download/)
- Хост: `127.0.0.1`
- База данных: `my-shows-rating`
- Пользователь: `postgres`
- Пароль: `123456`

Чтобы открыть Swagger - перейди по ссылке http://localhost/api/docs#/

*conftest.py* - содержит директорию, где лежат директории с фикстурами проекта
*BASE_URL* - базовый url, берется из переменных окружения (`.env` или `docker-compose.yml`)
*/data/insert_data_series.sql* - содержит скрипт для заполнения таблицы тестовыми данными

# Команды Allure
Для генерации отчета allure: *allure generate --clean allure-results/*
Для генерации 1 файлом: *allure generate --clean --single-file allure-results/*
Для запуска allure: *allure serve allure-results/*

# Команды Docker
Собрать и запустить все сервисы: *docker-compose up -d --build*
Посмотреть логи тестов: *docker-compose logs api-tests*
Посмотри логи всех сервисов в реальном времени: *docker-compose logs -f*
Остановить и удалить все: *docker-compose down*

Если хотим очистить папку на хосте от старых результатов тестов: 
*rm -rf allure-results/* && docker compose up -d --build api-tests*
