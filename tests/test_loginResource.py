import json
from user import User
from constants import Constants
from tests.base_test import BaseTestCase


class TestLoginResource(BaseTestCase):
    def test_login_with_correct_credentials(self):
        self.create_account()
        input_json = self.defaultUserJSON()
        result = self.app.post('/login', headers=input_json)
        data = json.loads(result.data)
        response_json = data['result']

        user = User(response_json)

        assert user.last_name == input_json[Constants.k_last_name]
        assert user.first_name == input_json[Constants.k_first_name]
        assert user.email == input_json[Constants.k_email]

    def test_login_with_wrong_email(self):
        self.create_account()
        input_json = self.defaultUserJSON()
        input_json[Constants.k_email] = 'wrong_email'
        result = self.app.post('/login', headers=input_json)

        assert result.status_code == 401

    def test_login_with_wrong_password(self):
        self.create_account()
        input_json = self.defaultUserJSON()
        input_json[Constants.k_password] = 'wrong_password'
        result = self.app.post('/login', headers=input_json)

        assert result.status_code == 401

    def test_login_empty_email(self):
        self.create_account()
        input_json = self.defaultUserJSON()
        input_json[Constants.k_email] = ''
        result = self.app.post('/login', headers=input_json)

        assert result.status_code == 401

    def test_login_emtpy_password(self):
        self.create_account()
        input_json = self.defaultUserJSON()
        input_json[Constants.k_password] = ''
        result = self.app.post('/login', headers=input_json)

        assert result.status_code == 401

    def test_login_email_not_approved(self):
        self.create_account(is_email_approved = False)
        input_json = self.defaultUserJSON()
        result = self.app.post('/login', headers=input_json)

        assert result.status_code == 401