import pytest

from api.burger_api import BurgerApi
from helpers import generate_user_data


@pytest.fixture
def register_user():
    tokens = []

    def register(data):
        response = BurgerApi.register_user(data)

        if response.status_code == 200:
            token = response.json().get("accessToken")
            if token:
                tokens.append(token)

        return response

    yield register

    errors = []

    for token in tokens:
        try:
            response = BurgerApi.delete_user(token)
            response.raise_for_status()
        except Exception as error:
            errors.append(str(error))

    if errors:
        raise RuntimeError(
            "Не удалось удалить тестовых пользователей: "
            + "; ".join(errors)
        )


@pytest.fixture
def registered_user(register_user):
    data = generate_user_data()
    response = register_user(data)
    response.raise_for_status()
    body = response.json()

    if body.get("success") is not True or not body.get("accessToken"):
        raise RuntimeError(
            f"Не удалось подготовить пользователя: {response.text}"
        )

    return {
        "data": data,
        "token": body["accessToken"],
    }