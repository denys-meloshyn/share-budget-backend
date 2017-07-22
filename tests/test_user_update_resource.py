from group import Group
from tests.base_test import BaseTestCase
from user_group import UserGroup
from users import User


class TestUserUpdateResource(BaseTestCase):
    def test_users(self):
        self.login()

        user = User({})
        user.email = "EMAIL_A"
        user.first_name = "USER_A"

        self.add_and_safe(user)

        group = Group({})
        group.name = "GROUP_A"
        self.add_and_safe(group)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)
