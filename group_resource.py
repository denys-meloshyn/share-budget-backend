from flask_restful import Resource
from flask_restful import reqparse

from group import Group
from constants import Constants
from shared_objects import swagger_app


def put_parameters(parser):
    parser.add_argument(Group.k_group_id, type=int, help='Group ID (if empty new group will be created)',
                        location='form')
    parser.add_argument(Constants.k_is_removed, type=bool, help='Is group removed',
                        location='form')
    parser.add_argument(Group.k_modified_user_id, type=int, help='Last modified user ID', location='form',
                        required=True)
    parser.add_argument(Group.k_name, type=str, help='Group name', location='form', required=True)


class GroupResource(Resource):
    parser = swagger_app.parser()
    put_parameters(parser)

    @swagger_app.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()

        return {}