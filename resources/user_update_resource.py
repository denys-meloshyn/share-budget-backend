from flask_restplus import Resource
from flask_restful import inputs
from flask_restful import reqparse

from model.user_group import UserGroup
from model.users import User
from utility.constants import Constants
from utility.credentials_validator import CredentialsValidator
from utility.resource_parser import ResourceParser
from utility.response_formatter import ResponseFormatter
from utility.shared_objects import api, db


def get_parameters(parser):
    parser.add_argument(Constants.JSON.time_stamp, type=inputs.iso8601interval, help='Time stamp date (ISO 8601)',
                        location='headers')

    ResourceParser.add_default_update_parameters(parser)


get_parser = reqparse.RequestParser()
swagger_get_parser = api.parser()

get_parameters(get_parser)
get_parameters(swagger_get_parser)


class UserUpdateResource(Resource):
    @api.doc(parser=swagger_get_parser)
    def get(self):
        args = get_parser.parse_args()

        user_id = args[Constants.JSON.user_id]
        token = args[Constants.JSON.token]
        status, message = CredentialsValidator.is_user_credentials_valid(user_id, token)

        if status is False:
            return message, 401

        subquery = db.session.query(UserGroup.group_id).filter(UserGroup.user_id == user_id).subquery()
        query = db.and_(User.user_id == UserGroup.user_id, UserGroup.group_id.in_(subquery))

        time_stamp = args.get(Constants.JSON.time_stamp)
        if type(time_stamp) is tuple:
            time_stamp = time_stamp[0].replace(tzinfo=None)
            query = db.session.query(User).filter(query, User.time_stamp >= time_stamp)
        else:
            query = db.session.query(User).filter(query)
        query = query.order_by(User.time_stamp.asc())

        start_page = args[Constants.JSON.pagination_start]
        page_size = args[Constants.JSON.pagination_page_size]

        return ResponseFormatter.format_response(query=query, start_page=start_page, page_size=page_size)
