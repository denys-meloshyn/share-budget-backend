from model.group import Group
from model.user import User
from model.user_group import UserGroup
from tests.base_test import BaseTestCase
from utility.constants import Constants
from utility.token_serializer import TokenSerializer


class TestUserUpdateResource(BaseTestCase):
    def parse_result(self, response):
        result = BaseTestCase.result(response)

        items = [UserGroup(item) for item in result]
        for i in range(len(items)):
            item = items[i]
            json = result[i]
            item.user_group_id = json[Constants.JSON.user_group_id]
        return items

    def create_user_group(self, user, group):
        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group.group_id
        self.add_and_save(user_group)

        return user_group

    def setUp(self):
        super(self.__class__, self).setUp()
        self.expected_result = []

    def test_all_users_in_one_group(self):
        user = BaseTestCase.create_user()
        access_token, refresh_token = TokenSerializer.access_refresh_token(user.user_id)

        # ----------------

        group = Group({})
        group.name = "GROUP_A"
        self.add_and_save(group)

        user_group = self.create_user_group(user=user, group=group)
        self.expected_result.append(user_group)

        # ----------------

        user_a = User({})
        user_a.first_name = "USER_A"
        self.add_and_save(user_a)

        user_group = self.create_user_group(user=user_a, group=group)
        self.expected_result.append(user_group)

        # ----------------

        user_b = User({})
        user_b.first_name = "USER_B"
        self.add_and_save(user_b)

        user_group = self.create_user_group(user=user_b, group=group)
        self.expected_result.append(user_group)

        headers = BaseTestCase.default_user_json(user)
        headers.update(BaseTestCase.access_token_header(access_token=access_token))
        response = self.test_client.get('/v1/user/group/updates', headers=headers)

        actual_result = self.parse_result(response)
        assert self.expected_result == actual_result

    def test_no_groups(self):
        current_user = BaseTestCase.create_user()
        access_token, refresh_token = TokenSerializer.access_refresh_token(current_user.user_id)

        # ----------------

        user = User({})
        user.first_name = "USER_A"
        self.add_and_save(user)

        # ----------------

        user = User({})
        user.first_name = "USER_B"
        self.add_and_save(user)

        # ----------------

        user = User({})
        user.first_name = "USER_C"
        self.add_and_save(user)

        headers = BaseTestCase.default_user_json(user)
        headers.update(BaseTestCase.access_token_header(access_token=access_token))
        response = self.test_client.get('/v1/user/group/updates', headers=headers)

        result = self.result(response)
        assert len(result) == 0

    def test_group_empty(self):
        current_user = BaseTestCase.create_user()
        access_token, refresh_token = TokenSerializer.access_refresh_token(current_user.user_id)

        group = Group({})
        group.name = "GROUP_1"
        self.add_and_save(group)

        # ----------------

        user = User({})
        user.first_name = "USER_1"
        self.add_and_save(user)

        # ----------------

        user = User({})
        user.first_name = "USER_2"
        self.add_and_save(user)

        # ----------------

        user = User({})
        user.first_name = "USER_3"
        self.add_and_save(user)

        headers = BaseTestCase.default_user_json(user)
        headers.update(BaseTestCase.access_token_header(access_token=access_token))
        response = self.test_client.get('/v1/user/group/updates', headers=headers)

        result = self.result(response)
        assert len(result) == 0

    def test_user_group_only_creator(self):
        current_user = BaseTestCase.create_user()
        access_token, refresh_token = TokenSerializer.access_refresh_token(current_user.user_id)

        group = Group({})
        group.name = "GROUP_1"
        self.add_and_save(group)

        # ----------------

        user_group = self.create_user_group(user=current_user, group=group)
        self.expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_1"
        self.add_and_save(user)

        # ----------------

        user = User({})
        user.first_name = "USER_2"
        self.add_and_save(user)

        # ----------------

        user = User({})
        user.first_name = "USER_3"
        self.add_and_save(user)

        headers = BaseTestCase.default_user_json(user)
        headers.update(BaseTestCase.access_token_header(access_token=access_token))
        response = self.test_client.get('/v1/user/group/updates', headers=headers)

        actual_result = self.parse_result(response)
        assert self.expected_result == actual_result

    def test_user_group_not_all_users(self):
        current_user = BaseTestCase.create_user()
        access_token, refresh_token = TokenSerializer.access_refresh_token(current_user.user_id)

        group = Group({})
        group.name = "GROUP_1"
        self.add_and_save(group)

        # ----------------

        user_group = self.create_user_group(user=current_user, group=group)
        self.expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_1"
        self.add_and_save(user)

        user_group = self.create_user_group(user=user, group=group)
        self.expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_2"
        self.add_and_save(user)

        # ----------------

        user = User({})
        user.first_name = "USER_3"
        self.add_and_save(user)

        user_group = self.create_user_group(user=current_user, group=group)
        self.expected_result.append(user_group)

        # ----------------

        headers = BaseTestCase.default_user_json(user)
        headers.update(BaseTestCase.access_token_header(access_token=access_token))
        response = self.test_client.get('/v1/user/group/updates', headers=headers)

        actual_result = self.parse_result(response)
        assert self.expected_result == actual_result

    def test_single_user_in_multiple_groups(self):
        current_user = BaseTestCase.create_user()
        access_token, refresh_token = TokenSerializer.access_refresh_token(current_user.user_id)

        group_1 = Group({})
        group_1.name = "GROUP_1"
        self.add_and_save(group_1)

        group_2 = Group({})
        group_2.name = "GROUP_2"
        self.add_and_save(group_2)

        group_3 = Group({})
        group_3.name = "GROUP_3"
        self.add_and_save(group_3)

        group_4 = Group({})
        group_4.name = "GROUP_3"
        self.add_and_save(group_4)

        # ----------------

        user_group = self.create_user_group(user=current_user, group=group_1)
        self.expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_1"
        self.add_and_save(user)

        user_group = self.create_user_group(user=user, group=group_2)
        self.expected_result.append(user_group)

        user_group = self.create_user_group(user=current_user, group=group_2)
        self.expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_2"
        self.add_and_save(user)

        user_group = self.create_user_group(user=user, group=group_3)
        self.add_and_save(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_3"
        self.add_and_save(user)

        user_group = self.create_user_group(user=user, group=group_4)
        self.expected_result.append(user_group)

        user_group = self.create_user_group(user=current_user, group=group_4)
        self.expected_result.append(user_group)

        # ----------------

        headers = BaseTestCase.default_user_json(user)
        headers.update(BaseTestCase.access_token_header(access_token=access_token))
        response = self.test_client.get('/v1/user/group/updates', headers=headers)

        actual_result = self.parse_result(response)
        assert self.expected_result == actual_result

    def test_multiple_users_in_multiple_groups(self):
        current_user = BaseTestCase.create_user()
        access_token, refresh_token = TokenSerializer.access_refresh_token(current_user.user_id)

        group_1 = Group({})
        group_1.name = "GROUP_1"
        self.add_and_save(group_1)

        group_2 = Group({})
        group_2.name = "GROUP_2"
        self.add_and_save(group_2)

        group_3 = Group({})
        group_3.name = "GROUP_3"
        self.add_and_save(group_3)

        group_4 = Group({})
        group_4.name = "GROUP_3"
        self.add_and_save(group_4)

        # ----------------

        user_group = self.create_user_group(user=current_user, group=group_1)
        self.expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_1"
        self.add_and_save(user)

        user_group = self.create_user_group(user=user, group=group_2)
        self.expected_result.append(user_group)

        user_group = self.create_user_group(user=current_user, group=group_2)
        self.expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_2"
        self.add_and_save(user)

        user_group = self.create_user_group(user=user, group=group_3)
        self.expected_result.append(user_group)

        user_group = self.create_user_group(user=current_user, group=group_3)
        self.expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_3"
        self.add_and_save(user)

        self.create_user_group(user=user, group=group_4)

        # ----------------

        headers = BaseTestCase.default_user_json(user)
        headers.update(BaseTestCase.access_token_header(access_token=access_token))
        response = self.test_client.get('/v1/user/group/updates', headers=headers)

        actual_result = self.parse_result(response)
        assert self.expected_result == actual_result
