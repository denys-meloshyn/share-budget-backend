from unittest import TestCase

from flask import json

from main import flask_app
from model.users import User
from utility.constants import Constants
from utility.shared_objects import db


class BaseTestCase(TestCase):
    @staticmethod
    def configure_app():
        flask_app.testing = True
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/postgres_test'

    def setUp(self):
        self.configure_app()
        self.test_client = flask_app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self):
        self.create_account()
        self.test_client.post('/login', headers=self.default_user_json())

    def create_account(self, is_email_approved=True, json_attr=None):
        if json_attr is None:
            json_attr = self.default_user_json()

        user = User(json_attr)
        user.is_email_approved = is_email_approved

        db.session.add(user)
        db.session.commit()
        return user

    def default_user(self):
        json_attr = self.default_user_json()
        email = json_attr[Constants.k_email]
        items = User.query.filter(User.email == email)
        user = items[0]

        return user

    @staticmethod
    def result(response):
        data = json.loads(response.data)
        return data[Constants.k_result]

    @staticmethod
    def add_and_safe(model):
        db.session.add(model)
        db.session.commit()

    @staticmethod
    def default_user_json(user=None):
        json_attr = {Constants.k_first_name: 'test_first_name',
                     Constants.k_last_name: 'test_last_name',
                     Constants.k_email: 'test_email',
                     Constants.k_password: 'test_password'}
        if user is not None:
            json_attr[Constants.k_user_id] = user.user_id
            json_attr[Constants.k_token] = user.token

        return json_attr
