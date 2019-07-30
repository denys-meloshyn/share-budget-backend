from flask_restplus import Resource, reqparse

from application import api
from model import db
from model.category import Category
from utility.constants import Constants
from utility.credentials_validator import CredentialsValidator
from utility.resource_parser import ResourceParser


def put_parameters(parser):
    parser.add_argument(Constants.JSON.category_id, type=int, help='Category ID', location='form')
    parser.add_argument(Constants.JSON.group_id, type=int, help='Group ID', location='form', required=True)
    parser.add_argument(Constants.JSON.name, help='Category name', location='form', required=True)

    ResourceParser.add_default_parameters(parser)


class CategoryResource(Resource):
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

        category_id = args.get(Constants.JSON.category_id)
        if category_id is None:
            category = Category(args)
            db.session.add(category)
            db.session.commit()
        else:
            items = Category.query.filter(Category.category_id == category_id).all()

            if len(items) > 0:
                category = items[0]
                category.update(args)
                db.session.commit()
            else:
                return Constants.error_reponse('category_not_exist')

        return Constants.default_response(category.to_json())
