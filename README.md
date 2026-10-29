# Diplom_2 — API-тесты Stellar Burgers

## Проверяемые сценарии

Регистрация:
- создание уникального пользователя;
- повторная регистрация существующего пользователя;
- регистрация без каждого из обязательных полей.

Авторизация:
- вход зарегистрированного пользователя;
- вход с неверным email, паролем и обоими значениями.

Создание заказа:
- с ингредиентами, с авторизацией и без неё;
- без ингредиентов, с авторизацией и без неё;
- с неверным хешем ингредиента, с авторизацией и без неё.

Тестовые пользователи получают уникальные данные и удаляются после проверок.

## Структура

- `api/burger_api.py` — методы обращения к API.
- `api/endpoints.py` — пути эндпоинтов.
- `config.py` — адрес стенда и тайм-аут запросов.
- `conftest.py` — фикстуры.
- `tests/` — тесты регистрации, авторизации и заказов.

## Установка в Git Bash

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

## Запуск тестов

```bash
python -m pytest tests -v --alluredir=allure-results --clean-alluredir
```

## Allure-отчёт

Для построения отчёта необходимы установленный Allure CLI и Java.

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Результат проверенного прогона: 15 тестов успешно пройдены.

Стенд: https://qa-stellarburgers.education-services.ru# Diplom_2
