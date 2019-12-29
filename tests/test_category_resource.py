from model.category import Category
from model.group import Group
from tests.base_test import BaseTestCase
from utility.constants import Constants
from utility.token_serializer import TokenSerializer


class TestCategoryResource(BaseTestCase):
    def test_permission_allowed_to_create_category(self):
        user_a = BaseTestCase.create_user()
        access_token_a, refresh_token_a = TokenSerializer.access_refresh_token(user_a.user_id)

        # ----------------

        group_a = Group({})
        group_a.name = "GROUP_A"
        self.add_and_save(group_a)

        self.create_user_group(user=user_a, group=group_a)

        category = Category(input_parameters={})
        category.name = 'test'
        category.group_id = group_a.group_id

        # ----------------

        response = self.test_client.put('/v1/category',
                                        headers=BaseTestCase.access_token_header(access_token=access_token_a),
                                        data=category.to_json())

        assert response.json[Constants.JSON.result][Constants.JSON.category_id] == 1

    def test_permission_not_allowed_to_create_expense(self):
        user_a = BaseTestCase.create_user()

        # ----------------

        group_a = Group({})
        group_a.name = "GROUP_A"
        self.add_and_save(group_a)

        self.create_user_group(user=user_a, group=group_a)

        # ----------------

        user_b = BaseTestCase.create_user(apple_sign_in_id='user_b')
        access_token_b, refresh_token_b = TokenSerializer.access_refresh_token(user_b.user_id)

        # ----------------

        category = Category(input_parameters={})
        category.name = 'test'
        category.group_id = group_a.group_id

        response = self.test_client.put('/v1/category',
                                        headers=BaseTestCase.access_token_header(access_token=access_token_b),
                                        data=category.to_json())

        assert response.status_code == 401
        assert response.json == Constants.error_reponse('Permission not allowed')
