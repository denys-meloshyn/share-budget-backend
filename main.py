import os
from flask import Flask
from shared_objects import db
from shared_objects import mail
from shared_objects import passlib
from user_resource import UserResource
from shared_objects import swagger_app
from flask_restful import Api as FlaskApi

from flask_passlib import LazyCryptContext
from flask_passlib.context import werkzeug_salted_md5
from flask_passlib.context import werkzeug_salted_sha1
from flask_passlib.context import werkzeug_salted_sha256
from flask_passlib.context import werkzeug_salted_sha512


def add_resource(obj, path):
    swagger_app.add_resource(obj, path)
    flask_resource_api.add_resource(obj, path)

os.environ.setdefault("DATABASE_URL", "postgresql://localhost/postgres")

flask_app = Flask(__name__)
flask_app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
flask_app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='my_username@gmail.com',
    MAIL_PASSWORD='my_password',
))

flask_resource_api = FlaskApi(flask_app)

db.init_app(flask_app)
with flask_app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    db.create_all()

swagger_app.init_app(flask_app)

passlib.init_app(flask_app, context=LazyCryptContext(
    schemes=[
        werkzeug_salted_md5,
        werkzeug_salted_sha1,
        werkzeug_salted_sha256,
        werkzeug_salted_sha512,
    ],
    default='werkzeug_salted_sha512',))

mail.init_app(flask_app)

add_resource(UserResource, '/user')

if __name__ == '__main__':
    flask_app.run(debug=True)
