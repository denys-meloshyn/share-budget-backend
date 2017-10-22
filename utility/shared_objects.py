import os
from flask import Flask, Blueprint
from flask_mail import Mail
from flask_passlib import Passlib
from flask_passlib.handlers import werkzeug_salted_md5, werkzeug_salted_sha1, werkzeug_salted_sha256, \
    werkzeug_salted_sha512
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from passlib.context import LazyCryptContext

from utility.constants import Constants

app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
app.config['BUNDLE_ERRORS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://localhost/postgres')
app.config.update(dict(
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

mail = Mail(app)

db = SQLAlchemy(app)
app.app_context().push()
db.create_all()

passlib = Passlib(app, context=LazyCryptContext(
    schemes=[
        werkzeug_salted_md5,
        werkzeug_salted_sha1,
        werkzeug_salted_sha256,
        werkzeug_salted_sha512,
    ],
    default='werkzeug_salted_sha512',))
