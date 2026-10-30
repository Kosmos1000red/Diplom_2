from uuid import uuid4

from api.burger_api import BurgerApi


def generate_user_data():
    unique_id = uuid4().hex

    return {
        "email": f"test_{unique_id}@example.com",
        "password": f"Password_{unique_id}",
        "name": "Тестовый пользователь",
    }


def get_ingredient_ids():
    response = BurgerApi.get_ingredients()
    response.raise_for_status()
    body = response.json()

    if body.get("success") is not True:
        raise RuntimeError(
            f"Не удалось получить ингредиенты: {response.text}"
        )

    ingredients = body["data"]
    bun = next(
        item["_id"] for item in ingredients
        if item["type"] == "bun"
    )
    filling = next(
        item["_id"] for item in ingredients
        if item["type"] == "main"
    )

    return [bun, filling, bun]