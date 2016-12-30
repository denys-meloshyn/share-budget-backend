import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api as FlaskApi
from flask_restplus import Api as SwaggerApi

from user_resource import UserResource

class SharedObjects:
    __instance = None

    def __init__(self):
        if SharedObjects.__instance:
            raise Exception('Use instance function')

        self.flask_app = Flask(__name__)
        self.swagger_app = SwaggerApi()
        self.db = SQLAlchemy(self.flask_app)
        self.flask_resource_api = FlaskApi(self.flask_app)

        self.configure_flask_app()
        self.configure_database()
        self.configure_swagger()

        self.configure_resource_path()

    @staticmethod
    def instance():
        if not SharedObjects.__instance:
            return SharedObjects()

        return SharedObjects.__instance

    def configure_flask_app(self):
        self.flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    def configure_database(self):
        with self.flask_app.app_context():
            # Extensions like Flask-SQLAlchemy now know what the "current" app
            self.db.create_all()

    def configure_swagger(self):
        self.swagger_app.init_app(self.flask_app)

        self.swagger_app.add_resource(UserResource, '/user')

    def configure_resource_path(self):
        # self.flask_resource_api.init_app(self.flask_app)

        self.flask_resource_api.add_resource(UserResource, '/user')
