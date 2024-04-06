import allure

from data import ingredients, API_URL
from helper import OrderRequests


class TestCreateOrder:

    @allure.title('Создание заказа с ингредиентами (с авторизацией)')
    @allure.description('Expected: 200 и order.number и order.owner')
    @allure.link(API_URL.ORDERS)
    def test_create_order_after_auth(self, user_registration):
        user_data, headers = user_registration
        response = OrderRequests.create_order(ingredients=ingredients, headers=headers)

        status_code = response.status_code
        actual_success = response.json()['success']
        order_data = response.json()['order']
        assert status_code == 200 and actual_success == True and 'number' in order_data and 'owner' in order_data

    @allure.title('Создание заказа с ингредиентами (БЕЗ авторизации)')
    @allure.description('Expected: 200 и order.number')
    @allure.link(API_URL.ORDERS)
    def test_create_order_without_auth_correct_ingredients(self):
        response = OrderRequests.create_order(ingredients=ingredients)

        status_code = response.status_code
        actual_success = response.json()['success']
        order_data = response.json()['order']
        assert status_code == 200 and actual_success == True and 'number' in order_data

    @allure.title('Создание заказа без ингредиентов (c авторизацией)')
    @allure.description('Expected: 400 и Ingredient ids must be provided')
    @allure.link(API_URL.ORDERS)
    def test_create_order_after_auth_correct_ingredients(self, user_registration):
        user_data, headers = user_registration
        response = OrderRequests.create_order(headers=headers)

        status_code = response.status_code
        message = response.json()['message']
        expected_message = "Ingredient ids must be provided"
        assert status_code == 400 and expected_message in message

    @allure.title('Создание заказа c невалидныv хэшем ингредиента (c авторизацией)')
    @allure.description('Expected: 500 и Internal Server Error')
    @allure.link(API_URL.ORDERS)
    def test_create_order_after_auth_incorrect_ingredients(self, user_registration):
        user_data, headers = user_registration
        ingredients['ingredients'] = ["test_value"]
        response = OrderRequests.create_order(ingredients=ingredients, headers=headers)

        status_code = response.status_code
        expected_message = "Internal Server Error"
        assert status_code == 500 and expected_message in response.text


class GetUserOrders:
    @allure.title('Получение списка заказов для конкретного пользователя(с авторизацией)')
    @allure.description('Expected: 200 и заказ есть в списке')
    @allure.link(API_URL.ORDERS)
    def test_get_user_orders_after_auth(self, user_registration):
        user_data, headers = user_registration
        # Создаём заказ
        create_order = OrderRequests.create_order(ingredients=ingredients, headers=headers)
        order_number = create_order.json()['order']['number']
        # Получаем список заказов этого пользователя
        response = OrderRequests.get_request_orders(headers=headers)

        status_code = response.status_code
        user_orders = response.json()['orders']
        assert status_code == 200 and user_orders[-1]['number'] == order_number

    @allure.title('Получение списка заказов для конкретного пользователя (БЕЗ авторизации)')
    @allure.description('Expected: 401 и You should be authorised')
    @allure.link(API_URL.ORDERS)
    def test_get_user_orders_without_auth(self):
        response = OrderRequests.get_request_orders()

        status_code = response.status_code
        message = response.json()['message']
        expected_message = "You should be authorised"
        assert status_code == 401 and message == expected_message
