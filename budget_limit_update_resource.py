from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from group import Group
from shared_objects import db
from constants import Constants
from shared_objects import swagger_app
from credentials_validator import CredentialsValidator


def get_parameters(get_parser):
    get_parser.add_argument(Group.k_group_id, type=int, help='Group ID', required=True)
    get_parser.add_argument(Constants.k_time_stamp, type=str, help='Time stamp date (ISO 8601)',
                            location='headers', required=True)

    get_parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='headers', required=True)
    get_parser.add_argument(Constants.k_token, type=str, help='User token', location='headers', required=True)


class BudgetLimitUpdateResource(Resource):
    parser = swagger_app.parser()
    get_parameters(parser)

    @swagger_app.doc(parser=parser)
    def get(self):
        get_parser = reqparse.RequestParser()
        get_parameters(get_parser)
        args = get_parser.parse_args()

        user_id = args[Constants.k_user_id]
        token = args[Constants.k_token]
        status, message = CredentialsValidator.is_user_credentials_valid(user_id, token)

        # if status is False:
        #     return message

        # group_id = args.get(Group.k_group_id)

        return {}
