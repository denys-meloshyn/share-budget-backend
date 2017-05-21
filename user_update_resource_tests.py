import unittest
from main import flask_app

class UserUpdateResourceTests(unittest.TestCase):

    def setUp(self):
        self.app = flask_app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_login(self):
        result = self.app.post('/login', headers={'email': 'ned19881@gmail.com', 'password':'1'}, follow_redirects=True)
        print result.data

if __name__ == '__main__':
    unittest.main()