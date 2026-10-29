from uuid import uuid4

import pytest

from api.burger_api import BurgerApi


@pytest.fixture
def user_data():
    unique_id = uuid4().hex
    return {
        "email": f"test_{unique_id}@example.com",
        "password": f"Password_{unique_id}",
        "name": "Тестовый пользователь",
    }


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

    for token in tokens:
        response = BurgerApi.delete_user(token)
        assert response.status_code == 202, (
            "Не удалось удалить тестового пользователя: "
            f"{response.status_code}, {response.text}"
        )


@pytest.fixture
def registered_user(user_data, register_user):
    response = register_user(user_data)

    assert response.status_code == 200, (
        f"Не удалось создать пользователя: {response.text}"
    )
    body = response.json()
    assert body["success"] is True

    return {
        "data": user_data,
        "token": body["accessToken"],
    }

@pytest.fixture
def ingredient_ids():
    response = BurgerApi.get_ingredients()

    assert response.status_code == 200, response.text

    body = response.json()
    assert body["success"] is True

    ingredients = body["data"]
    bun = next(item["_id"] for item in ingredients if item["type"] == "bun")
    filling = next(
        item["_id"] for item in ingredients if item["type"] == "main"
    )

    return [bun, filling, bun]