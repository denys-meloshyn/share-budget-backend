from unittest import TestCase

from flask import json

import app
from application import create_app
from model import db
from model.user import User
from utility.constants import Constants
from utility.token_serializer import TokenSerializer


class BaseTestCase(TestCase):
    def create_app(self):
        return create_app()

    @staticmethod
    def configure_app():
        app.flask_app.testing = True
        app.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'

    def setUp(self):
        self.configure_app()
        self.test_client = app.flask_app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self):
        user = self.create_account()
        access_token, refresh_token = TokenSerializer.access_refresh_token(user.user_id)
        return access_token

    @staticmethod
    def create_user(apple_sign_in_id='default_apple_sign_in_id'):
        user = User({})
        user.apple_sign_in_id = apple_sign_in_id

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def access_token_header(access_token):
        return {'Authorization': 'Bearer {}'.format(access_token)}

    def create_account(self, is_email_approved=True, json_attr=None):
        if json_attr is None:
            json_attr = self.default_user_json()

        user = User(json_attr)
        user.apple_sign_in_id = 'test_apple_sign_in_id'

        db.session.add(user)
        db.session.commit()
        return user

    def default_user(self):
        json_attr = self.default_user_json()
        email = json_attr[Constants.JSON.email]
        items = User.query.filter(User.email == email)
        user = items[0]

        return user

    @staticmethod
    def result(response):
        data = json.loads(response.data)
        return data[Constants.JSON.result]

    @staticmethod
    def add_and_safe(model):
        db.session.add(model)
        db.session.commit()

    @staticmethod
    def default_user_json(user=None):
        json_attr = {Constants.JSON.first_name: 'test_first_name',
                     Constants.JSON.last_name: 'test_last_name',
                     Constants.JSON.email: 'test_email',
                     Constants.JSON.password: 'test_password'}
        if user is not None:
            json_attr[Constants.JSON.user_id] = user.user_id
            # json_attr[Constants.JSON.token] = user.token

        return json_attr
