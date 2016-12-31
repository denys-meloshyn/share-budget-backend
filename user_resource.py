from user import User
from flask_restful import Resource
from flask_restful import reqparse
from shared_objects import db
from shared_objects import swagger_app


class UserResource(Resource):
    parser = swagger_app.parser()

    @swagger_app.doc(parser=parser)
    def get(self):
        return {'test': 1}

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstName', type=str, help='First Name', location='form', required=True)
        parser.add_argument('lastName', type=str, help='Last Name', location='form', required=True)
        parser.add_argument('password', type=str, help='Password', location='form', required=True)
        parser.add_argument('email', type=str, help='User email', location='form', required=True)
        args = parser.parse_args()

        user = User()
        db.session.add(user)
        db.session.commit()

        return user.to_json()
