from flask import json

from group import Group
from tests.base_test import BaseTestCase
from user_group import UserGroup
from users import User


class TestUserUpdateResource(BaseTestCase):
    def test_all_users_in_one_group(self):
        self.login()
        current_user = self.default_user()

        # ----------------

        group = Group({})
        group.name = "GROUP_A"
        self.add_and_safe(group)

        user_group = UserGroup({})
        user_group.user_id = current_user.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)
        expected_result = [user_group]

        # ----------------

        user = User({})
        user.first_name = "USER_A"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_B"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        response = self.test_client.get('/user/group/updates',
                                        headers=self.default_user_json(current_user))
        result = self.result(response)
        actual_result = []
        for item in result:
            user = UserGroup(item)
            actual_result.append(user)

        assert expected_result == actual_result
