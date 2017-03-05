from user import User
from shared_objects import db
from constants import Constants
from flask_restful import Resource
from flask_restful import reqparse
from shared_objects import swagger_app


def add_get_parameters(parser):
    parser.add_argument(Constants.k_token, help='Registration token', required=True)


class RegistrationEmailResource(Resource):
    get_parser = swagger_app.parser()
    add_get_parameters(get_parser)

    @swagger_app.doc(parser=get_parser)
    def get(self):
        parser = reqparse.RequestParser()
        add_get_parameters(parser)
        args = parser.parse_args()

        users = User.query.filter_by(registration_email_token=args[Constants.k_token]).all()
        if len(users) == 0:
            return Constants.error_reponse('user_doesnt_exist'), 401

        user = users[0]
        user.is_email_approved = True

        db.session.commit()

        return {Constants.k_message: 'email_registered'}
