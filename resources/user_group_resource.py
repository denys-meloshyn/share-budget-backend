from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from flask_restplus import Resource, reqparse

from application import api
from model import db
from model.group import Group
from model.user_group import UserGroup
from resources.group_resource import GroupResource
from utility.constants import Constants
from utility.resource_parser import ResourceParser


def put_parameters(parser):
    parser.add_argument(Constants.JSON.user_group_id, type=int, help='User group ID', location='form', required=True)
    parser.add_argument(Constants.JSON.group_id, type=int, help='Group ID', location='form', required=True)

    ResourceParser.add_default_parameters(parser)


class UserGroupResource(Resource):
    parser = api.parser()
    put_parameters(parser)

    @staticmethod
    def can_modify_user_group(sender_user_id, user_group_to_modify):
        return user_group_to_modify.user_id == sender_user_id

    @jwt_required
    @api.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()
        user_id = get_jwt_identity()

        user_group_id = args.get(Constants.JSON.user_group_id)
        items = UserGroup.query.filter_by(user_group_id=user_group_id).all()

        if len(items) == 0:
            return Constants.error_reponse('user_group_is_not_exist'), 401

        user_group = items[0]

        groups = Group.query.filter_by(group_id=user_group.group_id).all()
        if len(groups) == 0:
            return Constants.error_reponse(Constants.JSON.group_is_not_exist), 401

        if not GroupResource.can_modify_group(user_id, groups[0]):
            return Constants.error_reponse(Constants.JSON.user_is_not_creator_of_entity), 401

        user_group.update(args)
        db.session.commit()

        return Constants.default_response(user_group.to_json())
