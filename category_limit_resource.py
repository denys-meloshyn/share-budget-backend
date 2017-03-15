from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from shared_objects import db
from constants import Constants
from shared_objects import swagger_app
from category_limit import CategoryLimit
from credentials_validator import CredentialsValidator


def put_parameters(parser):
    parser.add_argument(Constants.k_category_limit_id, type=int, help='Category limit ID', location='form')
    parser.add_argument(Constants.k_category_id, type=int, help='Category ID', location='form', required=True)
    parser.add_argument(Constants.k_limit, type=float, help='Category limit', location='form', required=True)
    parser.add_argument(Constants.k_date, type=inputs.date, help='Category limit date', location='form', required=True)

    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
    parser.add_argument(Constants.k_token, help='User token', location='form', required=True)
    parser.add_argument(Constants.k_is_removed, type=inputs.boolean, help='Is group limit removed', location='form')
    parser.add_argument(Constants.k_internal_id, type=int, help='Internal ID', location='form')


class CategoryLimitResource(Resource):
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

        category_limit_id = args.get(Constants.k_category_id)
        if category_limit_id is None:
            category_limit = CategoryLimit(args)
            db.session.add(category_limit)
            db.session.commit()
        else:
            items = CategoryLimit.query.filter(CategoryLimit.category_limit_id == category_limit_id).all()

            if len(items) > 0:
                category_limit = items[0]
                category_limit.update(args)
                db.session.commit()
            else:
                return Constants.error_reponse('category_limit_not_exist')

        return Constants.default_response(category_limit.to_json())
