import allure
import pytest


@allure.feature("Регистрация пользователя")
class TestRegistration:
    @allure.title("Создание пользователя с уникальным email")
    def test_create_unique_user(self, user_data, register_user):
        response = register_user(user_data)

        assert response.status_code == 200, response.text

        body = response.json()

        assert body["success"] is True
        assert body["user"] == {
            "email": user_data["email"],
            "name": user_data["name"],
        }
        assert body.get("accessToken")
        assert body.get("refreshToken")

    @allure.title("Повторная регистрация существующего пользователя")
    def test_create_existing_user(self, registered_user, register_user):
        response = register_user(registered_user["data"])

        assert response.status_code == 403, response.text
        assert response.json() == {
            "success": False,
            "message": "User already exists",
        }

    @allure.title("Регистрация без обязательного поля: {field}")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_create_user_without_required_field(
        self, user_data, register_user, field
    ):
        data = user_data.copy()
        data.pop(field)

        response = register_user(data)

        assert response.status_code == 403, response.text
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields",
        }