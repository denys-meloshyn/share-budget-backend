import os
from flask import Flask
from flask_passlib.handlers import werkzeug_salted_md5, werkzeug_salted_sha1, werkzeug_salted_sha256, \
    werkzeug_salted_sha512
from passlib.context import LazyCryptContext

from apis.api_v1 import namespace as namespace_1
from utility.constants import Constants
from utility.shared_objects import api, blueprint, db, mail, passlib

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

db.init_app(app)
app.app_context().push()
db.create_all()

mail.init_app(app)

passlib.init_app(app, context=LazyCryptContext(
    schemes=[
        werkzeug_salted_md5,
        werkzeug_salted_sha1,
        werkzeug_salted_sha256,
        werkzeug_salted_sha512,
    ],
    default='werkzeug_salted_sha512',))


api.add_namespace(namespace_1)
# api.add_namespace(namespace_2)

app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)
