from datetime import datetime

from sqlalchemy import orm

from model import db
from utility.constants import Constants


class User(db.Model):
    __tablename__ = 'USER'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)
    apple_sign_in_id = db.Column(db.Text)

    @orm.reconstructor
    def init_on_load(self):
        self.internal_id = None

    def __init__(self, input_parameters):
        self.internal_id = None
        self.is_removed = False
        self.update(input_parameters)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False

        if self.user_id != other.user_id:
            return False

        if self.first_name != other.first_name:
            return False

        if self.last_name != other.last_name:
            return False

        if self.email != other.email:
            return False

        if self.is_removed != other.is_removed:
            return False

        return True

    def __repr__(self):
        return '(user_id={}, first_name={}, last_name={}, email={}, is_removed={})'.format(self.user_id,
                                                                                           self.first_name,
                                                                                           self.last_name,
                                                                                           self.email,
                                                                                           self.is_removed)

    def update(self, new_value):
        value = new_value.get(Constants.JSON.email)
        if value is not None:
            self.email = value

        value = new_value.get(Constants.JSON.last_name)
        if value is not None:
            self.last_name = value

        value = new_value.get(Constants.JSON.first_name)
        if value is not None:
            self.first_name = value

        value = new_value.get(Constants.JSON.is_removed)
        if value is not None:
            self.is_removed = value
        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {Constants.JSON.user_id: self.user_id,
                       Constants.JSON.first_name: self.first_name,
                       Constants.JSON.last_name: self.last_name,
                       Constants.JSON.email: self.email,
                       Constants.JSON.is_removed: self.is_removed}

        if self.time_stamp is not None:
            json_object[Constants.JSON.time_stamp] = self.time_stamp.isoformat()

        return json_object

    @staticmethod
    def find(email):
        return User.query.filter_by(email=email).first()
