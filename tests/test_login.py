import allure

from api.burger_api import BurgerApi
from helpers import generate_user_data


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

    @allure.title("Вход с неверным email")
    def test_login_with_wrong_email(self, registered_user):
        unknown_user = generate_user_data()

        response = BurgerApi.login_user({
            "email": unknown_user["email"],
            "password": registered_user["data"]["password"],
        })

        assert response.status_code == 401, response.text
        assert response.json() == {
            "success": False,
            "message": "email or password are incorrect",
        }

    @allure.title("Вход с неверным паролем")
    def test_login_with_wrong_password(self, registered_user):
        other_data = generate_user_data()

        response = BurgerApi.login_user({
            "email": registered_user["data"]["email"],
            "password": other_data["password"],
        })

        assert response.status_code == 401, response.text
        assert response.json() == {
            "success": False,
            "message": "email or password are incorrect",
        }

    @allure.title("Вход с неверными email и паролем")
    def test_login_with_wrong_email_and_password(self, registered_user):
        unknown_user = generate_user_data()

        response = BurgerApi.login_user({
            "email": unknown_user["email"],
            "password": unknown_user["password"],
        })

        assert response.status_code == 401, response.text
        assert response.json() == {
            "success": False,
            "message": "email or password are incorrect",
        }