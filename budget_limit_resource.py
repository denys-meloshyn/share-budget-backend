from flask_restful import inputs
from dateutil.parser import parse
from flask_restful import Resource
from flask_restful import reqparse

from group import Group
from shared_objects import db
from constants import Constants
from budget_limit import BudgetLimit
from shared_objects import swagger_app
from credentials_validator import CredentialsValidator


def get_parameters(get_parser):
    get_parser.add_argument(Group.k_group_id, type=int, help='Group ID', required=True)
    get_parser.add_argument(BudgetLimit.k_date, type=inputs.date, help='Limit date', required=True)

    get_parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='headers', required=True)
    get_parser.add_argument(Constants.k_token, type=str, help='User token', location='headers', required=True)


def put_parameters(parser):
    parser.add_argument(Group.k_group_id, type=int, help='Group ID', location='form', required=True)
    parser.add_argument(BudgetLimit.k_limit, type=float, help='Limit', location='form', required=True)
    parser.add_argument(BudgetLimit.k_date, type=str, help='Limit date', location='form', required=True)

    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
    parser.add_argument(Constants.k_token, type=str, help='User token', location='form', required=True)
    parser.add_argument(Constants.k_is_removed, type=inputs.boolean, help='Is group limit removed', location='form')


class BudgetLimitResource(Resource):
    get_parser = swagger_app.parser()
    get_parameters(get_parser)

    @swagger_app.doc(parser=get_parser)
    def get(self):
        get_parser = reqparse.RequestParser(bundle_errors=True)
        get_parameters(get_parser)
        args = get_parser.parse_args()

        print args

        user_id = args[Constants.k_user_id]
        token = args[Constants.k_token]
        status, message = CredentialsValidator.is_user_credentials_valid(user_id, token)

        if status is False:
            return message

        print args.get(BudgetLimit.k_date)
        date = args.get(BudgetLimit.k_date).replace(day=1)

        group_id = args.get(Group.k_group_id)

        items = BudgetLimit.query.filter(db.and_(BudgetLimit.date <= date, BudgetLimit.group_id == group_id))
        if items.count() == 0:
            return Constants.error_reponse('group_limit_not_found'), 401
        else:
            budget_limit = items[-1]
            budget_limit.update(args)

            return Constants.default_response(budget_limit.to_json())

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
            return message

        date = parse(args.get(BudgetLimit.k_date)).replace(day=1)
        group_id = args.get(Group.k_group_id)

        items = BudgetLimit.query.filter(db.and_(BudgetLimit.date <= date, BudgetLimit.group_id == group_id))
        if items.count() == 0:
            budget_limit = BudgetLimit(args)
            db.session.add(budget_limit)
        else:
            budget_limit = items[0]
            budget_limit.update(args)

        db.session.commit()
        return Constants.default_response(budget_limit.to_json())
