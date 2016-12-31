from user import User
from shared_objects import db
from constants import Constants
from flask_restful import Resource
from flask_restful import reqparse
from shared_objects import swagger_app


def put_parameters(parser):
    parser.add_argument('firstName', type=str, help='First Name', location='form', required=True)
    parser.add_argument('lastName', type=str, help='Last Name', location='form')
    parser.add_argument('password', type=str, help='Password', location='form', required=True)
    parser.add_argument('email', type=str, help='User email', location='form', required=True)


class UserResource(Resource):
    # def get(self):
    #     return {'test': 1}

    parser = swagger_app.parser()
    put_parameters(parser)

    @swagger_app.doc(parser=parser)
    def put(self):
        parser = reqparse.RequestParser()
        put_parameters(parser)
        args = parser.parse_args()

        user = User(args)

        items = User.query.filter_by(email=user.email).all()
        if len(items) > 0:
            return Constants.error_message('user_is_already_exist', 401)

        db.session.add(user)
        db.session.commit()

        return user.to_json()
