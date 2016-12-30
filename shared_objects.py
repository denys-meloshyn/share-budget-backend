import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class SharedObjects:
    __instance = None

    def __init__(self):
        if SharedObjects.__instance:
            raise Exception('Use instance function')

        self.db = SQLAlchemy()
        self.flask_app = Flask(__name__)

        self.configure_flask_app()
        self.configure_database()

    @staticmethod
    def instance():
        if not SharedObjects.__instance:
            return SharedObjects()

        return SharedObjects.__instance

    def configure_flask_app(self):
        self.flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    def configure_database(self):
        self.db.init_app(self.flask_app)
