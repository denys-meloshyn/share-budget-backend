from flask_restplus import Resource, reqparse, inputs

from model import db
from model.budget_limit import BudgetLimit
from utility.constants import Constants
from utility.credentials_validator import CredentialsValidator
from utility.resource_parser import ResourceParser
from utility.shared_objects import api


def put_parameters(parser):
    parser.add_argument(Constants.JSON.group_id, type=int, help='Group ID', location='form', required=True)
    parser.add_argument(Constants.JSON.limit, type=float, help='Limit', location='form', required=True)
    parser.add_argument(Constants.JSON.date, type=inputs.date, help='Limit date', location='form', required=True)

    ResourceParser.add_default_parameters(parser)


class BudgetLimitResource(Resource):
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

        date = args.get(Constants.JSON.date).replace(day=1)
        group_id = args.get(Constants.JSON.group_id)

        items = BudgetLimit.query.filter(db.and_(BudgetLimit.date == date, BudgetLimit.group_id == group_id))
        if items.count() == 0:
            budget_limit = BudgetLimit(args)
            db.session.add(budget_limit)
        else:
            budget_limit = items[0]
            budget_limit.update(args)

        db.session.commit()
        return Constants.default_response(budget_limit.to_json())
