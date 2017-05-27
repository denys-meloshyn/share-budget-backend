import json

from constants import Constants
from tests.base_test import BaseTestCase


class TestUserResource(BaseTestCase):
    def test_create_existed_user(self):
        self.create_account()

        response = self.app.post('/user', content_type='multipart/form-data', data=self.defaultUserJSON())
        data = json.loads(response.data)

        assert response.status_code == 401
        assert data[Constants.k_message] == Constants.k_user_is_already_exist
