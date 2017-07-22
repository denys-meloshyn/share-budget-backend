import unittest

import json

from constants import Constants
from users import User
from main import flask_app
from shared_objects import db

class UserUpdateResourceTests(unittest.TestCase):

    def setUp(self):
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/postgres_test'
        self.db = db

        self.db.init_app(flask_app)
        with flask_app.app_context():
            # Extensions like Flask-SQLAlchemy now know what the "current" app
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
        user = User({Constants.k_first_name: 'test_first_name',
                     Constants.k_last_name: 'test_last_name',
                     Constants.k_email: 'test_email',
                     Constants.k_password: 'test_password'})
        user.is_email_approved = True

        with flask_app.app_context():
            db.session.add(user)
            db.session.commit()
        # response = self.app.post('/user', content_type='multipart/form-data', data={'email': 'test_user@gmail.com',
        #                              'password': 'test_password',
        #                              'firstName': 'test_first_name'})
        # print response.data

    def test_login(self):
        self.create_account()
        input_json = self.defaultUserJSON()
        result = self.app.post('/login', headers=input_json)
        data = json.loads(result.data)
        response_json = data['result']

        user = User(response_json)

        assert user.last_name == input_json[Constants.k_last_name]

if __name__ == '__main__':
    unittest.main()