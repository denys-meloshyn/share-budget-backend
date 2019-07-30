from flask_restplus import Resource, inputs, reqparse

from application import api
from model import db
from model.expense import Expense
from utility.constants import Constants
from utility.credentials_validator import CredentialsValidator
from utility.resource_parser import ResourceParser


def put_parameters(parser):
    parser.add_argument(Constants.JSON.expense_id, type=int, help='Expense ID (if empty new expense will be created)',
                        location='form')
    parser.add_argument(Constants.JSON.category_id, type=int, help='Category ID', location='form')
    parser.add_argument(Constants.JSON.group_id, type=int, help='Group ID', location='form', required=True)
    parser.add_argument(Constants.JSON.name, help='Expense name', location='form', required=True)
    parser.add_argument(Constants.JSON.price, type=float, help='Expense price', location='form', required=True)
    parser.add_argument(Constants.JSON.creation_date, type=inputs.iso8601interval, help='Expense creation date',
                        location='form', required=True)

    ResourceParser.add_default_parameters(parser)


class ExpenseResource(Resource):
    parser = api.parser()
    put_parameters(parser)

    @api.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()

        user_id = args[Constants.JSON.user_id]
        token = args[Constants.JSON.token]
        status, message = CredentialsValidator.is_user_credentials_valid(user_id, token)

        if status is False:
            return message, 401

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
