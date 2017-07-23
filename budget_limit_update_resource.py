from flask_restful import Resource
from flask_restful import reqparse


from constants import Constants
from response_formatter import ResponseFormatter
from user_group import UserGroup
from budget_limit import BudgetLimit
from shared_objects import swagger_app
from credentials_validator import CredentialsValidator
from utility.resource_parser import ResourceParser


def get_parameters(parser):
    ResourceParser.add_default_update_parameters(parser)


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
            return message, 401

        query = BudgetLimit.query.filter(user_id == UserGroup.user_id, UserGroup.group_id == BudgetLimit.group_id)

        time_stamp = args.get(Constants.k_time_stamp)
        if time_stamp is not None:
            time_stamp = time_stamp[0].replace(tzinfo=None)
            query = query.from_self().filter(BudgetLimit.time_stamp >= time_stamp)
        query = query.order_by(BudgetLimit.time_stamp.asc())

        start_page = args[Constants.k_pagination_start]
        page_size = args[Constants.k_pagination_page_size]

        return ResponseFormatter.format_response(query=query, start_page=start_page, page_size=page_size)
