from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from group import Group
from shared_objects import db
from constants import Constants
from shared_objects import swagger_app
from credentials_validator import CredentialsValidator


def put_parameters(parser):
    parser.add_argument(Group.k_group_id, type=int, help='Group ID (if empty new group will be created)',
                        location='form')
    parser.add_argument(Group.k_name, type=str, help='Group name', location='form', required=True)

    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
    parser.add_argument(Constants.k_token, type=str, help='User token', location='form', required=True)
    parser.add_argument(Constants.k_is_removed, type=inputs.boolean, help='Is group limit removed', location='form')


class GroupResource(Resource):
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

        group_id = args.get(Group.k_group_id)
        if group_id is None:
            group = Group(args)
            db.session.add(group)
            db.session.commit()
        else:
            items = Group.query.filter_by(group_id=group_id).all()

            if len(items) == 0:
                return Constants.error_reponse('group_is_not_exist'), 401

            group = items[0]
            group.update(args)
            db.session.commit()

        return Constants.default_response(group.to_json())
