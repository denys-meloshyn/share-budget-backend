from flask_restplus import Resource, reqparse

from model.category import Category
from model.group import Group
from model.user_group import UserGroup
from utility.constants import Constants
from utility.credentials_validator import CredentialsValidator
from utility.resource_parser import ResourceParser
from utility.shared_objects import api


def put_parameters(parser):
    parser.add_argument(Constants.JSON.group_id, type=int, help='Group ID (if empty new group will be created)',
                        location='form')
    parser.add_argument(Constants.JSON.name, help='Group name', location='form', required=True)

    ResourceParser.add_default_parameters(parser)


class GroupResource(Resource):
    parser = api.parser()
    put_parameters(parser)

    @staticmethod
    def can_modify_group(sender_user_id, group_to_modify):
        return group_to_modify.creator_user_id == sender_user_id

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
