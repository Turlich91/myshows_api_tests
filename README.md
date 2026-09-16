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
*/data/api_config.py* - содержит базовый url
*/data/test_data_series.sql* - содержит скрипт для заполнения таблицы тестовыми данными

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

