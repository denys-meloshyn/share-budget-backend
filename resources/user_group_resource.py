from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from flask_restplus import Resource, reqparse

from application import api
from model import db
from model.group import Group
from model.user_group import UserGroup
from utility.constants import Constants
from utility.resource_parser import ResourceParser


def put_parameters(parser):
    parser.add_argument(Constants.JSON.user_group_id, type=int, help='User group ID', location='form')
    parser.add_argument(Constants.JSON.user_id, type=int, help='User ID', location='form', required=True)
    parser.add_argument(Constants.JSON.group_id, type=int, help='Group ID', location='form', required=True)

    ResourceParser.add_default_parameters(parser)


class UserGroupResource(Resource):
    parser = api.parser()
    put_parameters(parser)

    @jwt_required
    @api.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()
        request_user_id = get_jwt_identity()

        user_group_id = args.get(Constants.JSON.user_group_id)
        if user_group_id is None:
            user_group = UserGroup(input_parameters=args)
            db.session.add(user_group)
            db.session.commit()

            return Constants.default_response(user_group.to_json())

        user_group = UserGroup.query.filter_by(user_group_id=user_group_id).first()
        if not user_group:
            return Constants.error_reponse('user_group_is_not_exist'), 401

        group = Group.query.filter_by(group_id=user_group.group_id).first()
        if not group:
            return Constants.error_reponse(Constants.JSON.group_is_not_exist), 401

        if group.creator_user_id != request_user_id:
            return Constants.error_reponse(Constants.JSON.permission_not_allowed), 401

        user_group.update(args)
        db.session.commit()

        return Constants.default_response(user_group.to_json())
