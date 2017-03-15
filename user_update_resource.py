from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from user import User
from shared_objects import db
from constants import Constants
from user_group import UserGroup
from shared_objects import swagger_app
from credentials_validator import CredentialsValidator


def get_parameters(parser):
    parser.add_argument(Constants.k_time_stamp, type=inputs.iso8601interval, help='Time stamp date (ISO 8601)',
                        location='headers')
    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='headers', required=True)
    parser.add_argument(Constants.k_token, help='User token', location='headers', required=True)


get_parser = reqparse.RequestParser()
swagger_get_parser = swagger_app.parser()

get_parameters(get_parser)
get_parameters(swagger_get_parser)


class UserUpdateResource(Resource):
    @swagger_app.doc(parser=swagger_get_parser)
    def get(self):
        args = get_parser.parse_args()

        user_id = args[Constants.k_user_id]
        token = args[Constants.k_token]
        status, message = CredentialsValidator.is_user_credentials_valid(user_id, token)

        if status is False:
            return message, 401

        subquery = db.session.query(UserGroup.group_id).filter(UserGroup.user_id == user_id).subquery()
        query = db.and_(User.user_id == UserGroup.user_id, UserGroup.group_id.in_(subquery))

        time_stamp = args.get(Constants.k_time_stamp)
        if time_stamp is not None:
            time_stamp = time_stamp[0].replace(tzinfo=None)
            items = db.session.query(User).filter(query, User.time_stamp >= time_stamp).filter().all()
        else:
            items = db.session.query(User).filter(query).filter().all()

        time_stamp = max(item.time_stamp for item in items)
        items = [model.to_json() for model in items]

        return Constants.default_response(items, time_stamp)
