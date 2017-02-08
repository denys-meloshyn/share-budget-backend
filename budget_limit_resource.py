from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from shared_objects import db
from constants import Constants
from budget_limit import BudgetLimit
from shared_objects import swagger_app
from credentials_validator import CredentialsValidator


def put_parameters(parser):
    parser.add_argument(Constants.k_group_id, type=int, help='Group ID', location='form', required=True)
    parser.add_argument(Constants.k_limit, type=float, help='Limit', location='form', required=True)
    parser.add_argument(Constants.k_date, type=inputs.date, help='Limit date', location='form', required=True)

    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
    parser.add_argument(Constants.k_token, type=str, help='User token', location='form', required=True)
    parser.add_argument(Constants.k_is_removed, type=inputs.boolean, help='Is group limit removed', location='form')
    parser.add_argument(Constants.k_internal_id, type=int, help='Internal ID', location='headers')


class BudgetLimitResource(Resource):
    parser = swagger_app.parser()
    put_parameters(parser)

    @swagger_app.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()

        user_id = args[Constants.k_user_id]
        token = args[Constants.k_token]
        status, message = CredentialsValidator.is_user_credentials_valid(user_id, token)

        if status is False:
            return message, 401

        date = args.get(Constants.k_date).replace(day=1)
        group_id = args.get(Constants.k_group_id)

        items = BudgetLimit.query.filter(db.and_(BudgetLimit.date == date, BudgetLimit.group_id == group_id))
        if items.count() == 0:
            budget_limit = BudgetLimit(args)
            db.session.add(budget_limit)
        else:
            budget_limit = items[0]
            budget_limit.update(args)

        db.session.commit()
        return Constants.default_response(budget_limit.to_json())
