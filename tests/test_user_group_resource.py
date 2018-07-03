from model.group import Group
from model.user_group import UserGroup
from model.users import User
from resources.user_group_resource import UserGroupResource
from tests.base_test import BaseTestCase


class TestUserGroupResource(BaseTestCase):
    def test_create_of_group_can_change_user_group(self):
        self.login()

        creator = self.default_user()

        group = Group({})
        group.name = 'Group A'
        group.creator_user_id = creator.user_id
        self.add_and_safe(group)

        user_group = UserGroup({})
        user_group.user_id = creator.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)

        self.assertTrue(UserGroupResource.can_modify_user_group(creator.user_id, user_group))

    def test_another_user_cant_change_user_group(self):
        self.login()

        creator = self.default_user()

        group = Group({})
        group.name = 'Group A'
        group.creator_user_id = creator.user_id
        self.add_and_safe(group)

        user_group = UserGroup({})
        user_group.user_id = creator.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)

        user_without_permission = User({})
        user_without_permission.first_name = 'user without permission to change user group'
        self.add_and_safe(user_without_permission)

        self.assertFalse(UserGroupResource.can_modify_user_group(user_without_permission.user_id, user_group))
