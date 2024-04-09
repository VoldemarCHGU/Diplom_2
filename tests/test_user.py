import allure
import pytest

from data import API_URL
from helper import UserRequests


class TestCreateUser:

    @allure.title('Создание нового уникального пользователя')
    @allure.description('Успешная регистрация возвращает accessToken')
    @allure.link(API_URL.CREATE_USER)
    def test_create_uniq_user(self, generate_user_data):
        user_data = generate_user_data
        response = UserRequests.create_user(data=user_data)
        status_code = response.status_code
        assert status_code == 200 and 'accessToken' in response.text

    @allure.title('Регистрация пользователя, который уже зарегистрирован')
    @allure.description('expected: 403 User already exists')
    @allure.link(API_URL.CREATE_USER)
    def test_create_exists_user(self, generate_user_data):
        user_data = generate_user_data
        # Регистрируем 1ого пользователя для независмиости текущей базы на разных площадках
        UserRequests.create_user(data=user_data)

        # Отправляем на регистрацию те же данные
        response = UserRequests.create_user(data=user_data)
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 403 and message == "User already exists"

    @allure.title('Регистрация пользователя без одного из обязательных полей')
    @allure.description('expected: 403 Email, password and name are required fields')
    @allure.link(API_URL.CREATE_USER)
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_user_without_requirement_field(self, generate_user_data, field):
        user_data = generate_user_data
        user_data[field] = None

        response = UserRequests.create_user(data=user_data)
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 403 and message == "Email, password and name are required fields"


class TestLoginUser:

    @allure.title('Проверка авторизации пользователя')
    @allure.description('Ожидается: 200 и "success"=true')
    @allure.link(API_URL.LOGIN_USER)
    def test_login_user_with_correct_data(self, user_registration):
        user_data, _ = user_registration
        response = UserRequests.user_auth(user_data)

        expected_success = True
        actual_success = response.json()['success']
        assert response.status_code == 200 and expected_success == actual_success

    @allure.title('Проверяем, что система вернёт ошибку, если неправильно указать email или пароль')
    @allure.description('Ожидается: 401 и "email or password are incorrect"')
    @allure.link(API_URL.LOGIN_USER)
    @pytest.mark.parametrize('field', ['email', 'password'])
    def test_login_user_with_incorrect_data(self, user_registration, field):
        user_data, _ = user_registration
        user_data[field] = user_data[field] + '_test'
        response = UserRequests.user_auth(user_data)

        expected = {'success': False, 'message': "email or password are incorrect"}
        assert response.status_code == 401 and expected == response.json()


class TestPathUser:
    @allure.title('Проверка изменения данных пользователя с авторизацией')
    @allure.description('Меняем: email, name, password'
                        'expected: 200 и новые поля пользователя (без пароля в ответе)')
    @allure.link(API_URL.USER_PATCH_OR_DELETE)
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_user_patch_authorized(self, user_registration, generate_user_data, field):
        user_data, headers = user_registration
        # Присваиваем новое значение для пользователя
        user_data[field] = generate_user_data[field]
        # Отправляем запрос c headers (для авторизации)
        response = UserRequests.patch_user(data=user_data, headers=headers)

        expected_data = {'success': True, 'user': {'name': user_data['name'], 'email': user_data['email']}}
        assert response.status_code == 200 and response.json() == expected_data

    @allure.title('Проверка изменения данных пользователя без авторизации')
    @allure.description('Меняем: email, name, password.'
                        'Expected: 401 - You should be authorised')
    @allure.link(API_URL.USER_PATCH_OR_DELETE)
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_user_patch_unauthorized(self, user_registration, generate_user_data, field):
        user_data, _ = user_registration
        # Присваиваем новое значение для пользователя
        user_data[field] = generate_user_data[field]
        # Отправляем запрос без headers (без авторизации)
        response = UserRequests.patch_user(data=user_data)

        expected_data = {'success': False, 'message': 'You should be authorised'}
        assert response.status_code == 401 and response.json() == expected_data
