from unittest import TestCase

import json

from flask import Response

from user import User
from main import flask_app
from shared_objects import db
from constants import Constants


class TestLoginResource(TestCase):
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

    def defaultUserJSON(self):
        return {Constants.k_first_name: 'test_first_name',
                Constants.k_last_name: 'test_last_name',
                Constants.k_email: 'test_email',
                Constants.k_password: 'test_password'}

    def create_account(self):
        user = User(self.defaultUserJSON())
        user.is_email_approved = True

        with flask_app.app_context():
            db.session.add(user)
            db.session.commit()

    def test_login_with_correct_credentials(self):
        self.create_account()
        input_json = self.defaultUserJSON()
        result = self.app.post('/login', headers=input_json)
        data = json.loads(result.data)
        response_json = data['result']

        user = User(response_json)

        assert user.last_name == input_json[Constants.k_last_name]
        assert user.first_name == input_json[Constants.k_first_name]
        assert user.email == input_json[Constants.k_email]

    def test_login_with_wrong_email(self):
        self.create_account()
        input_json = self.defaultUserJSON()
        input_json[Constants.k_email] = 'wrong_email'
        result = self.app.post('/login', headers=input_json)

        assert result.status_code == 401

    def test_login_with_wrong_password(self):
        self.create_account()
        input_json = self.defaultUserJSON()
        input_json[Constants.k_password] = 'wrong_password'
        result = self.app.post('/login', headers=input_json)

        assert result.status_code == 401

    def test_login_empty_email(self):
        self.create_account()
        input_json = self.defaultUserJSON()
        input_json[Constants.k_email] = ''
        result = self.app.post('/login', headers=input_json)

        assert result.status_code == 401

    def test_login_etmpy_password(self):
        self.create_account()
        input_json = self.defaultUserJSON()
        input_json[Constants.k_password] = ''
        result = self.app.post('/login', headers=input_json)

        assert result.status_code == 401
