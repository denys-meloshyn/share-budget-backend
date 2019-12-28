from tests.base_test import BaseTestCase
from utility.constants import Constants


class TestLoginResource(BaseTestCase):
    def test_login_with_wrong_email(self):
        self.create_account()
        input_json = self.default_user_json()
        input_json[Constants.JSON.email] = 'wrong_email'
        result = self.test_client.post('/v1/login', headers=input_json)

        assert result.status_code == 401

    def test_login_empty_email(self):
        self.create_account()
        input_json = self.default_user_json()
        input_json[Constants.JSON.email] = ''
        result = self.test_client.post('/v1/login', headers=input_json)

        assert result.status_code == 401
