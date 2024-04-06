import pytest

from helper import RandomUserData, UserRequests


@pytest.fixture
def generate_user_data():
    user = RandomUserData()
    user_data = user.get_user_info()
    return user_data


@pytest.fixture
def user_registration(generate_user_data):
    user_data = generate_user_data
    response = UserRequests.create_user(data=user_data)
    headers = {'Authorization': response.json()["accessToken"]}
    yield user_data, headers
    UserRequests.delete_user(headers=headers)
