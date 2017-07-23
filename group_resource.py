from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from group import Group
from shared_objects import db
from category import Category
from constants import Constants
from user_group import UserGroup
from shared_objects import swagger_app
from credentials_validator import CredentialsValidator
from utility.resource_parser import ResourceParser


def put_parameters(parser):
    parser.add_argument(Constants.k_group_id, type=int, help='Group ID (if empty new group will be created)',
                        location='form')
    parser.add_argument(Constants.k_name, help='Group name', location='form', required=True)

    ResourceParser.add_default_parameters(parser)


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
            return message, 401

        group_id = args.get(Constants.k_group_id)
        # If group_id exist?
        if group_id is None:
            # No: create new group row
            group = Group(args)
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
                return Constants.error_reponse('group_is_not_exist'), 401

            group = items[0]
            group.update(args)
            db.session.commit()

        return Constants.default_response(group.to_json())
