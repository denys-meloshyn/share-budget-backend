import os

from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from flask_restplus import Api
from passlib.context import CryptContext
from sentry_sdk import init

from model import db

jwt = JWTManager()
blueprint = Blueprint('api', __name__)
api = Api(blueprint)

pwd_context = CryptContext(
    # Replace this list with the hash(es) you wish to support.
    # this example sets pbkdf2_sha256 as the default,
    # with additional support for reading legacy des_crypt hashes.
    schemes=["pbkdf2_sha256", "des_crypt"],

    # Automatically mark all but first hasher in list as deprecated.
    # (this will be the default in Passlib 2.0)
    deprecated="auto",

    # Optionally, set the number of rounds that should be used.
    # Appropriate values may vary for different schemes,
    # and the amount of time you wish it to take.
    # Leaving this alone is usually safe, and will use passlib's defaults.
    ## pbkdf2_sha256__rounds = 29000,
)


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    flask_app.config['BUNDLE_ERRORS'] = True
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                                 'postgresql://localhost/voltage_counter')
    flask_app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

    db.init_app(app=flask_app)
    jwt.init_app(app=flask_app)
    jwt._set_error_handler_callbacks(api)

    from apis.api_v1 import namespace
    api.add_namespace(namespace)
    flask_app.register_blueprint(blueprint)

    init(os.environ['SENTRY'])

    return flask_app
