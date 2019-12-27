import json

from model.user import User
from tests.base_test import BaseTestCase
from utility.constants import Constants


class TestLoginResource(BaseTestCase):
    def test_login_with_correct_credentials(self):
        self.create_account()
        input_json = self.default_user_json()
        result = self.test_client.post('/v1/login', headers=input_json)
        data = json.loads(result.data)
        response_json = data['result']

        user = User(response_json)

        assert user.last_name == input_json[Constants.JSON.last_name]
        assert user.first_name == input_json[Constants.JSON.first_name]
        assert user.email == input_json[Constants.JSON.email]

    def test_login_with_wrong_email(self):
        self.create_account()
        input_json = self.default_user_json()
        input_json[Constants.JSON.email] = 'wrong_email'
        result = self.test_client.post('/v1/login', headers=input_json)

        assert result.status_code == 401

    def test_login_with_wrong_password(self):
        self.create_account()
        input_json = self.default_user_json()
        input_json[Constants.JSON.password] = 'wrong_password'
        result = self.test_client.post('/v1/login', headers=input_json)

        assert result.status_code == 401

    def test_login_empty_email(self):
        self.create_account()
        input_json = self.default_user_json()
        input_json[Constants.JSON.email] = ''
        result = self.test_client.post('/v1/login', headers=input_json)

        assert result.status_code == 401

    def test_login_emtpy_password(self):
        self.create_account()
        input_json = self.default_user_json()
        input_json[Constants.JSON.password] = ''
        result = self.test_client.post('/v1/login', headers=input_json)

        assert result.status_code == 401

    def test_login_email_not_approved(self):
        self.create_account(is_email_approved=False)
        input_json = self.default_user_json()
        result = self.test_client.post('/v1/login', headers=input_json)

        assert result.status_code == 401
