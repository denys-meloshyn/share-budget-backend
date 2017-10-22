from unittest import TestCase

from flask import json

from app import app
from model.users import User
from utility.constants import Constants
from utility.shared_objects import db


class BaseTestCase(TestCase):
    @staticmethod
    def configure_app():
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/postgres_test'

    def setUp(self):
        self.configure_app()
        self.test_client = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self):
        self.create_account()
        self.test_client.post('/v1/login', headers=self.default_user_json())

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
            json_attr[Constants.JSON.token] = user.token

        return json_attr
