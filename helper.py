import random
import string

import allure
import requests

from data import API_URL


class RandomUserData:
    def __init__(self):
        self.name = "Vladimir"
        self.email = self.__generate_random_login()
        self.password = self.__generate_random_password_valid()

    def __generate_random_login(self):
        """Генератор логина/почты"""
        random_digit = random.randint(100, 999)
        all_symbols = string.ascii_lowercase
        result = ''.join(random.choice(all_symbols) for _ in range(random.randint(1, 5)))
        email = f"vladimir_nikolaev_diplom_{random_digit}@{result}.com"
        return email

    def __generate_random_password_valid(self):
        """Генератор валидного пароля"""
        all_symbols = string.ascii_letters + string.digits
        result = ''.join(random.choice(all_symbols) for _ in range(random.randint(6, 20)))
        return result

    def get_user_info(self, key=None):
        """для получения данных из класса"""
        data = {"name": self.name, "email": self.email, "password": self.password}
        if key:
            return data[key]
        return {"name": self.name, "email": self.email, "password": self.password}


class UserRequests:
    @allure.step('Создание нового пользователя')
    def create_user(data):
        return requests.post(API_URL.CREATE_USER, data=data)

    @allure.step(f'Удаление пользователя')
    def delete_request_user(data):
        return requests.delete(API_URL.USER_PATCH_OR_DELETE, headers=data)

    @allure.step('Авторизация пользователя')
    def user_auth(data):
        return requests.post(API_URL.LOGIN_USER, data=data)

    @allure.step('Редактирование пользователя')
    def patch_user(data, headers=None):
        return requests.patch(API_URL.USER_PATCH_OR_DELETE,
                              headers=headers, data=data)

    @allure.step(f'Удаление пользователя')
    def delete_user(headers):
        return requests.delete(API_URL.USER_PATCH_OR_DELETE, headers=headers)


class OrderRequests:

    @allure.step(f'Создаём заказ')
    def create_order(ingredients=None, headers=None):
        return requests.post(API_URL.ORDERS, data=ingredients, headers=headers, )

    @allure.step(f'Запрашиваем список заказов')
    def get_request_orders(headers=None):
        return requests.get(API_URL.ORDERS, headers=headers)
