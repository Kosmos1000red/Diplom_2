import allure
import requests

from config import BASE_URL, REQUEST_TIMEOUT
from api import endpoints


class BurgerApi:
    @staticmethod
    @allure.step("Зарегистрировать пользователя")
    def register_user(data):
        return requests.post(
            BASE_URL + endpoints.REGISTER,
            json=data,
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    @allure.step("Авторизовать пользователя")
    def login_user(data):
        return requests.post(
            BASE_URL + endpoints.LOGIN,
            json=data,
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    @allure.step("Удалить тестового пользователя")
    def delete_user(token):
        return requests.delete(
            BASE_URL + endpoints.USER,
            headers={"Authorization": token},
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    @allure.step("Получить список ингредиентов")
    def get_ingredients():
        return requests.get(
            BASE_URL + endpoints.INGREDIENTS,
            timeout=REQUEST_TIMEOUT,
        )

    @staticmethod
    @allure.step("Создать заказ")
    def create_order(data, token=None):
        headers = {}
        if token is not None:
            headers["Authorization"] = token

        return requests.post(
            BASE_URL + endpoints.ORDERS,
            json=data,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )