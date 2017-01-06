from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from group import Group
from constants import Constants
from budget_limit import BudgetLimit
from shared_objects import swagger_app
from credentials_validator import CredentialsValidator


def get_parameters(parser):
    parser.add_argument(Group.k_group_id, type=str, location='headers', required=True)
    parser.add_argument(Constants.k_time_stamp, type=inputs.iso8601interval, help='Time stamp date (ISO 8601)',
                        location='headers', required=True)

    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='headers', required=True)
    parser.add_argument(Constants.k_token, type=str, help='User token', location='headers', required=True)


get_parser = reqparse.RequestParser()
swagger_get_parser = swagger_app.parser()

get_parameters(get_parser)
get_parameters(swagger_get_parser)


class BudgetLimitUpdateResource(Resource):
    @swagger_app.doc(parser=swagger_get_parser)
    def get(self):
        args = get_parser.parse_args()

        user_id = args[Constants.k_user_id]
        token = args[Constants.k_token]
        status, message = CredentialsValidator.is_user_credentials_valid(user_id, token)

        if status is False:
            return message

        group_id = args.get(Group.k_group_id)
        time_stamp = args.get(Constants.k_time_stamp)
        if type(time_stamp) is tuple:
            time_stamp = time_stamp[0]

        items = BudgetLimit.query.filter(BudgetLimit.time_stamp > time_stamp, BudgetLimit.group_id == group_id).all()
        result = [model.to_json() for model in items]

        return Constants.default_response(result)
