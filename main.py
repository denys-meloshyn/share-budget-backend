import os
from flask import Flask
from shared_objects import db
from user_resource import UserResource
from shared_objects import swagger_app
from flask_restful import Api as FlaskApi

os.environ.setdefault("DATABASE_URL", "postgresql://localhost/postgres")

flask_app = Flask(__name__)
flask_app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

flask_resource_api = FlaskApi(flask_app)

db.init_app(flask_app)
with flask_app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    db.create_all()

swagger_app.init_app(flask_app)


def add_resource(obj, path):
    swagger_app.add_resource(obj, path)
    flask_resource_api.add_resource(obj, path)

add_resource(UserResource, '/user')

if __name__ == '__main__':
    flask_app.run(debug=True)
