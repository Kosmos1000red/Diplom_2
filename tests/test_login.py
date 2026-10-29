from uuid import uuid4

import allure
import pytest

from api.burger_api import BurgerApi


@allure.feature("Авторизация пользователя")
class TestLogin:
    @allure.title("Вход зарегистрированного пользователя")
    def test_login_existing_user(self, registered_user):
        user_data = registered_user["data"]

        response = BurgerApi.login_user({
            "email": user_data["email"],
            "password": user_data["password"],
        })

        assert response.status_code == 200, response.text

        body = response.json()

        assert body["success"] is True
        assert body["user"] == {
            "email": user_data["email"],
            "name": user_data["name"],
        }
        assert body.get("accessToken")
        assert body.get("refreshToken")

    @allure.title("Вход с неверными данными: {invalid_fields}")
    @pytest.mark.parametrize(
        "invalid_fields",
        [
            ("email",),
            ("password",),
            ("email", "password"),
        ],
        ids=["wrong_email", "wrong_password", "both_wrong"],
    )
    def test_login_with_invalid_credentials(
        self, registered_user, invalid_fields
    ):
        user_data = registered_user["data"]
        data = {
            "email": user_data["email"],
            "password": user_data["password"],
        }

        if "email" in invalid_fields:
            data["email"] = f"unknown_{uuid4().hex}@example.com"
        if "password" in invalid_fields:
            data["password"] = f"Wrong_{uuid4().hex}"

        response = BurgerApi.login_user(data)

        assert response.status_code == 401, response.text
        assert response.json() == {
            "success": False,
            "message": "email or password are incorrect",
        }