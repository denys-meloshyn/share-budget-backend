from datetime import datetime

from model.expense import Expense
from model.group import Group
from model.user_group import UserGroup
from tests.base_test import BaseTestCase
from utility.constants import Constants
from utility.token_serializer import TokenSerializer


class TestExpenseResource(BaseTestCase):
    def create_user_group(self, user, group):
        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group.group_id
        self.add_and_save(user_group)

        return user_group

    def test_permission_allowed_to_create_expense(self):
        user_a = BaseTestCase.create_user()
        access_token_a, refresh_token_a = TokenSerializer.access_refresh_token(user_a.user_id)

        # ----------------

        group_a = Group({})
        group_a.name = "GROUP_A"
        self.add_and_save(group_a)

        self.create_user_group(user=user_a, group=group_a)

        expense = Expense({})
        expense.price = 0
        expense.group_id = group_a.group_id
        expense.creation_date = datetime.utcnow()

        # ----------------

        response = self.test_client.put('/v1/expense',
                                        headers=BaseTestCase.access_token_header(access_token=access_token_a),
                                        data=expense.to_json())

        assert response.json[Constants.JSON.result][Constants.JSON.expense_id] == 1

    def test_permission_not_allowed_to_create_expense(self):
        user_a = BaseTestCase.create_user()

        # ----------------

        group_a = Group({})
        group_a.name = "GROUP_A"
        self.add_and_save(group_a)

        user_group = self.create_user_group(user=user_a, group=group_a)

        # ----------------

        user_b = BaseTestCase.create_user(apple_sign_in_id='user_b')
        access_token_b, refresh_token_b = TokenSerializer.access_refresh_token(user_b.user_id)

        # ----------------

        expense = Expense({})
        expense.price = 0
        expense.group_id = group_a.group_id
        expense.creation_date = datetime.utcnow()

        response = self.test_client.put('/v1/expense',
                                        headers=BaseTestCase.access_token_header(access_token=access_token_b),
                                        data=expense.to_json())

        assert response.status_code == 401
        assert response.json == Constants.error_reponse('Permission not allowed')
