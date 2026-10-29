import allure
import pytest

from api.burger_api import BurgerApi


@allure.feature("Создание заказа")
class TestOrders:
    @allure.title("Создание заказа с ингредиентами и авторизацией")
    def test_create_order_with_authorization(
        self, registered_user, ingredient_ids
    ):
        response = BurgerApi.create_order(
            {"ingredients": ingredient_ids},
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
    def test_create_order_without_authorization(self, ingredient_ids):
        response = BurgerApi.create_order(
            {"ingredients": ingredient_ids}
        )

        assert response.status_code == 200, response.text

        body = response.json()

        assert body["success"] is True
        assert isinstance(body["order"]["number"], int)
        assert body["order"]["number"] > 0

    @allure.title("Создание заказа без ингредиентов: {authorized}")
    @pytest.mark.parametrize(
        "authorized",
        [True, False],
        ids=["authorized", "unauthorized"],
    )
    def test_create_order_without_ingredients(
        self, authorized, request
    ):
        token = None
        if authorized:
            user = request.getfixturevalue("registered_user")
            token = user["token"]

        response = BurgerApi.create_order(
            {"ingredients": []},
            token=token,
        )

        assert response.status_code == 400, response.text
        assert response.json() == {
            "success": False,
            "message": "Ingredient ids must be provided",
        }

    @allure.title("Создание заказа с неверным хешем: {authorized}")
    @pytest.mark.parametrize(
        "authorized",
        [True, False],
        ids=["authorized", "unauthorized"],
    )
    def test_create_order_with_invalid_ingredient_hash(
        self, authorized, request
    ):
        token = None
        if authorized:
            user = request.getfixturevalue("registered_user")
            token = user["token"]

        response = BurgerApi.create_order(
            {"ingredients": ["invalid_ingredient_hash"]},
            token=token,
        )

        assert response.status_code == 500, response.text