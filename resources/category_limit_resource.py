from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from flask_restplus import Resource, inputs, reqparse

from application import api
from model import db
from model.category import Category
from model.category_limit import CategoryLimit
from model.user_group import UserGroup
from utility.constants import Constants
from utility.resource_parser import ResourceParser


def put_parameters(parser):
    parser.add_argument(Constants.JSON.category_limit_id, type=int, help='Category limit ID', location='form')
    parser.add_argument(Constants.JSON.category_id, type=int, help='Category ID', location='form', required=True)
    parser.add_argument(Constants.JSON.limit, type=float, help='Category limit', location='form', required=True)
    parser.add_argument(Constants.JSON.date,
                        type=inputs.date,
                        help='Category limit date',
                        location='form',
                        required=True)

    ResourceParser.add_default_parameters(parser)


class CategoryLimitResource(Resource):
    parser = api.parser()
    put_parameters(parser)

    @jwt_required
    @api.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()

        user_id = get_jwt_identity()
        category_id = args[Constants.JSON.category_id]

        category = Category.query.filter(Category.category_id == category_id).first()
        if category is None:
            return Constants.error_reponse(Constants.JSON.category_not_exist)

        if not UserGroup.is_user_part_of_group(user_id=user_id, group_id=category.group_id):
            return Constants.error_reponse(Constants.JSON.permission_not_allowed), 401

        category_limit_id = args[Constants.JSON.category_limit_id]
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
