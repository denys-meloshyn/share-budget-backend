from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from flask_restplus import Resource, reqparse

from application import api
from model import db
from model.category import Category
from model.group import Group
from model.user_group import UserGroup
from utility.constants import Constants
from utility.resource_parser import ResourceParser


def put_parameters(parser):
    parser.add_argument(Constants.JSON.group_id,
                        type=int,
                        help='Group ID (if empty new group will be created)',
                        location='form')
    parser.add_argument(Constants.JSON.name, help='Group name', location='form', required=True)
    ResourceParser.add_default_parameters(parser)


class GroupResource(Resource):
    parser = api.parser()
    put_parameters(parser)

    @staticmethod
    def can_modify_group(sender_user_id, group_to_modify):
        return group_to_modify.creator_user_id == sender_user_id

    @jwt_required()
    @api.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()
        user_id = get_jwt_identity()

        group_id = args.get(Constants.JSON.group_id)
        # If group_id exist?
        if group_id is None:
            # No: create new group row
            group = Group(args)
            group.creator_user_id = user_id
            db.session.add(group)
            db.session.commit()

            # Add user to the group
            user_group = UserGroup(dict())
            user_group.user_id = user_id
            user_group.group_id = group.group_id
            db.session.add(user_group)
            db.session.commit()

            # Add default categories to the group
            for category_name in Constants.default_categories:
                category = Category(dict())
                category.modified_user_id = user_id
                category.group_id = group.group_id
                category.name = category_name

                db.session.add(category)
                db.session.commit()
        else:
            items = Group.query.filter_by(group_id=group_id).all()

            if len(items) == 0:
                return Constants.error_reponse(Constants.JSON.group_is_not_exist), 401

            group = items[0]
            if not GroupResource.can_modify_group(user_id, group):
                return Constants.error_reponse(Constants.JSON.user_is_not_creator_of_entity), 401

            group.update(args)
            db.session.commit()

        return Constants.default_response(group.to_json())
