from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from shared_objects import db
from category import Category
from constants import Constants
from shared_objects import swagger_app
from credentials_validator import CredentialsValidator


def put_parameters(parser):
    parser.add_argument(Constants.k_category_id, type=int, help='Category ID', location='headers')
    parser.add_argument(Constants.k_group_id, type=int, help='Group ID', location='headers', required=True)
    parser.add_argument(Constants.k_name, type=str, help='Category name', location='headers', required=True)

    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='headers', required=True)
    parser.add_argument(Constants.k_token, type=str, help='User token', location='headers', required=True)
    parser.add_argument(Constants.k_is_removed, type=inputs.boolean, help='Is group limit removed', location='headers')
    parser.add_argument(Constants.k_internal_id, type=int, help='Internal ID', location='headers')


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
            return message

        category_id = args.get(Constants.k_category_id)
        if category_id is None:
            category = Category(args)
            db.session.add(category)
            db.session.commit()
        else:
            items = Category.query.filter(Category.category_id == category_id)

            if len(items) > 0:
                category = items[0]
                category.update(args)
                db.session.commit()
            else:
                return Constants.error_reponse('category_not_exist')

        return Constants.default_response(category.to_json())