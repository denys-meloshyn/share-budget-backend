from unittest import TestCase

from user import User
from main import flask_app
from shared_objects import db
from constants import Constants


class BaseTestCase(TestCase):
    def setUp(self):
        self.app = flask_app.test_client()
        self.app.testing = True
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/postgres_test'
        self.db = db

        self.db.init_app(flask_app)
        with flask_app.app_context():
            # Extensions like FlaskSQLAlchemy now know what the "current" app
            self.db.create_all()

            self.app = flask_app.test_client()
            self.app.testing = True

    def tearDown(self):
        with flask_app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def create_account(self, is_email_approved = True, json = None):
        if json is None:
            json = self.defaultUserJSON()

        user = User(json)
        user.is_email_approved = is_email_approved

        with flask_app.app_context():
            db.session.add(user)
            db.session.commit()

    def defaultUserJSON(self):
        return {Constants.k_first_name: 'test_first_name',
                Constants.k_last_name: 'test_last_name',
                Constants.k_email: 'test_email',
                Constants.k_password: 'test_password'}