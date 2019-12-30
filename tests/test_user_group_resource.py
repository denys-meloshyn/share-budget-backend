from model.group import Group
from model.user_group import UserGroup
from tests.base_test import BaseTestCase
from utility.constants import Constants
from utility.token_serializer import TokenSerializer


class TestUserGroupResource(BaseTestCase):
    def test_create_user_group(self):
        user_a = BaseTestCase.create_user()
        self.add_and_save(user_a)
        access_token_a, refresh_token_a = TokenSerializer.access_refresh_token(user_a.user_id)

        group = Group({})
        group.name = 'Group A'
        group.creator_user_id = user_a.user_id
        self.add_and_save(group)

        user_b = BaseTestCase.create_user(apple_sign_in_id='user_b')
        self.add_and_save(user_b)

        user_group = UserGroup({})
        user_group.user_id = user_b.user_id
        user_group.group_id = group.group_id

        response = self.test_client.put('/v1/user/group',
                                        headers=BaseTestCase.access_token_header(access_token=access_token_a),
                                        data=user_group.to_json())

        assert response.json[Constants.JSON.result][Constants.JSON.user_group_id] == 1

    def test_create_of_group_can_change_user_group(self):
        user_a = BaseTestCase.create_user()
        self.add_and_save(user_a)
        access_token_a, refresh_token_a = TokenSerializer.access_refresh_token(user_a.user_id)

        group = Group({})
        group.name = 'Group A'
        group.creator_user_id = user_a.user_id
        self.add_and_save(group)

        user_group = UserGroup({})
        user_group.user_id = user_a.user_id
        user_group.group_id = group.group_id
        self.add_and_save(user_group)

        response = self.test_client.put('/v1/user/group',
                                        headers=BaseTestCase.access_token_header(access_token=access_token_a),
                                        data=user_group.to_json())
        assert response.json[Constants.JSON.result][Constants.JSON.user_group_id] == 1

    def test_another_user_cant_change_user_group(self):
        user_a = BaseTestCase.create_user()

        group = Group({})
        group.name = 'Group A'
        group.creator_user_id = user_a.user_id
        self.add_and_save(group)

        user_group = UserGroup({})
        user_group.user_id = user_a.user_id
        user_group.group_id = group.group_id
        self.add_and_save(user_group)

        user_b = BaseTestCase.create_user(apple_sign_in_id='user_b')
        access_token_b, refresh_token_b = TokenSerializer.access_refresh_token(user_b.user_id)
        user_b.first_name = 'user without permission to change user group'
        self.add_and_save(user_b)

        response = self.test_client.put('/v1/user/group',
                                        headers=BaseTestCase.access_token_header(access_token=access_token_b),
                                        data=user_group.to_json())

        assert response.status_code == 401
        assert response.json == Constants.error_reponse(Constants.JSON.permission_not_allowed)
