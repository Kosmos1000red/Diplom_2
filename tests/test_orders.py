import allure

from api.burger_api import BurgerApi
from helpers import get_ingredient_ids


@allure.feature("Создание заказа")
class TestOrders:
    @allure.title("Создание заказа с ингредиентами и авторизацией")
    def test_create_order_with_authorization(self, registered_user):
        ingredients = get_ingredient_ids()

        response = BurgerApi.create_order(
            {"ingredients": ingredients},
            token=registered_user["token"],
        )

        assert response.status_code == 200, response.text

        body = response.json()

        assert body["success"] is True
        assert isinstance(body["order"]["number"], int)
        assert body["order"]["number"] > 0
        assert body["order"]["owner"]["email"] == (
            registered_user["data"]["email"]
        )

    @allure.title("Создание заказа с ингредиентами без авторизации")
    def test_create_order_without_authorization(self):
        ingredients = get_ingredient_ids()

        response = BurgerApi.create_order(
            {"ingredients": ingredients}
        )

        assert response.status_code == 200, response.text

        body = response.json()

        assert body["success"] is True
        assert isinstance(body["order"]["number"], int)
        assert body["order"]["number"] > 0

    @allure.title("Создание заказа без ингредиентов с авторизацией")
    def test_create_empty_order_with_authorization(self, registered_user):
        response = BurgerApi.create_order(
            {"ingredients": []},
            token=registered_user["token"],
        )

        assert response.status_code == 400, response.text
        assert response.json() == {
            "success": False,
            "message": "Ingredient ids must be provided",
        }

    @allure.title("Создание заказа без ингредиентов без авторизации")
    def test_create_empty_order_without_authorization(self):
        response = BurgerApi.create_order({"ingredients": []})

        assert response.status_code == 400, response.text
        assert response.json() == {
            "success": False,
            "message": "Ingredient ids must be provided",
        }

    @allure.title("Неверный хеш ингредиента с авторизацией")
    def test_invalid_hash_with_authorization(self, registered_user):
        response = BurgerApi.create_order(
            {"ingredients": ["invalid_ingredient_hash"]},
            token=registered_user["token"],
        )

        assert response.status_code == 500, response.text
        assert response.headers.get("Content-Type", "").startswith(
            "text/html"
        )
        assert "<pre>Internal Server Error</pre>" in response.text

    @allure.title("Неверный хеш ингредиента без авторизации")
    def test_invalid_hash_without_authorization(self):
        response = BurgerApi.create_order(
            {"ingredients": ["invalid_ingredient_hash"]}
        )

        assert response.status_code == 500, response.text
        assert response.headers.get("Content-Type", "").startswith(
            "text/html"
        )
        assert "<pre>Internal Server Error</pre>" in response.text