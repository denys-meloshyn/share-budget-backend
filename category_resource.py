from flask_restful import Resource
from flask_restful import reqparse

from category import Category
from shared_objects import db
from shared_objects import swagger_app
from utility.constants import Constants
from utility.credentials_validator import CredentialsValidator
from utility.resource_parser import ResourceParser


def put_parameters(parser):
    parser.add_argument(Constants.k_category_id, type=int, help='Category ID', location='form')
    parser.add_argument(Constants.k_group_id, type=int, help='Group ID', location='form', required=True)
    parser.add_argument(Constants.k_name, help='Category name', location='form', required=True)

    ResourceParser.add_default_parameters(parser)


class CategoryResource(Resource):
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

        category_id = args.get(Constants.k_category_id)
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
