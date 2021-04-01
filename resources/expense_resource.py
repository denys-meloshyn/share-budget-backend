from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from flask_restplus import Resource, inputs, reqparse

from application import api
from model import db
from model.expense import Expense
from model.user_group import UserGroup
from utility.constants import Constants
from utility.resource_parser import ResourceParser


def put_parameters(parser):
    parser.add_argument(Constants.JSON.expense_id,
                        type=int,
                        help='Expense ID (if empty new expense will be created)',
                        location='form')
    parser.add_argument(Constants.JSON.category_id, type=int, help='Category ID', location='form')
    parser.add_argument(Constants.JSON.group_id, type=int, help='Group ID', location='form', required=True)
    parser.add_argument(Constants.JSON.name, help='Expense name', location='form')
    parser.add_argument(Constants.JSON.price, type=float, help='Expense price', location='form', required=True)
    parser.add_argument(Constants.JSON.creation_date,
                        type=inputs.iso8601interval,
                        help='Expense creation date',
                        location='form',
                        required=True)

    ResourceParser.add_default_parameters(parser)


class ExpenseResource(Resource):
    parser = api.parser()
    put_parameters(parser)

    @jwt_required()
    @api.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()

        user_id = get_jwt_identity()
        group_id = args[Constants.JSON.group_id]

        if not UserGroup.is_user_part_of_group(user_id=user_id, group_id=group_id):
            return Constants.error_reponse(Constants.JSON.permission_not_allowed), 401

        expense_id = args.get(Constants.JSON.expense_id)
        # If expense_id exist?
        if expense_id is None:
            # No: create new expense row
            expense = Expense(args)
            db.session.add(expense)
            db.session.commit()
        else:
            items = Expense.query.filter_by(expense_id=expense_id).all()

            if len(items) == 0:
                return Constants.error_reponse('expense_is_not_exist'), 401

            expense = items[0]
            expense.update(args)
            db.session.commit()

        return Constants.default_response(expense.to_json())
