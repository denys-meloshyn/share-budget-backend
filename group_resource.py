from flask_restful import Resource
from flask_restful import reqparse

from shared_objects import swagger_app

# group_id: Integer, PK, AI
# modified_user_id: Integer
# budget_limit_id: Integer
# name: Varchar
# is_removed: Bool
# timestamp: DateTime

def put_parameters(parser):
    parser.add_argument('modified_user_id', type=str, help='Last Name', location='form')
    parser.add_argument('email', type=str, help='User email', location='form', required=True)
    parser.add_argument('password', type=str, help='Password', location='form', required=True)
    parser.add_argument('firstName', type=str, help='First Name', location='form', required=True)


class GroupResource(Resource):
    parser = swagger_app.parser()
    put_parameters(parser)

    @swagger_app.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()

        return {}