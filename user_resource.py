from user import User
from shared_objects import db
from flask_mail import Message
from constants import Constants
from shared_objects import mail
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
            return Constants.error_reponse('user_is_already_exist'), 401

        msg = Message('Hello', sender='ned1988@gmail.com', recipients=["ned1988@gmail.com"])
        mail.send(msg)

        db.session.add(user)
        db.session.commit()

        return Constants.default_response(user.to_json())
