import os

from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_passlib import Passlib
from flask_passlib.handlers import werkzeug_salted_md5, werkzeug_salted_sha1, werkzeug_salted_sha256, \
    werkzeug_salted_sha512
from flask_restplus import Api
from passlib.context import LazyCryptContext

from model import db
from utility.constants import Constants

flask_app = Flask(__name__)
flask_app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
flask_app.config['BUNDLE_ERRORS'] = True
flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
flask_app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['PROPAGATE_EXCEPTIONS'] = True
flask_app.config.update(dict(
    DEBUG=False,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=Constants.project_email,
    MAIL_PASSWORD='ShareBudgetTS',
))

blueprint = Blueprint('api', __name__)
api = Api(blueprint)

mail = Mail(flask_app)

jwt = JWTManager(app=flask_app)
jwt._set_error_handler_callbacks(api)

db.init_app(app=flask_app)
flask_app.app_context().push()

passlib = Passlib(flask_app, context=LazyCryptContext(
    schemes=[
        werkzeug_salted_md5,
        werkzeug_salted_sha1,
        werkzeug_salted_sha256,
        werkzeug_salted_sha512,
    ],
    default='werkzeug_salted_sha512', ))
