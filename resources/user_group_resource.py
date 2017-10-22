from flask_restplus import Resource, reqparse

from model.user_group import UserGroup
from utility.constants import Constants
from utility.credentials_validator import CredentialsValidator
from utility.resource_parser import ResourceParser
from utility.shared_objects import api, db


def put_parameters(parser):
    parser.add_argument(Constants.JSON.user_group_id, type=int, help='User group ID', location='form', required=True)
    parser.add_argument(Constants.JSON.group_id, type=int, help='Group ID', location='form', required=True)

    ResourceParser.add_default_parameters(parser)


class UserGroupResource(Resource):
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

        user_group_id = args.get(Constants.JSON.user_group_id)
        items = UserGroup.query.filter_by(user_group_id=user_group_id).all()

        if len(items) == 0:
            return Constants.error_reponse('user_group_is_not_exist'), 401

        user_group = items[0]
        user_group.update(args)
        db.session.commit()

        return Constants.default_response(user_group.to_json())
