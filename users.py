from sqlalchemy import orm
from datetime import datetime

from shared_objects import db
from constants import Constants
from shared_objects import passlib
from token_serializer import TokenSerializer


class User(db.Model):
    __tablename__ = 'USER'

    user_id = db.Column(db.Integer, primary_key=True)
    is_email_approved = db.Column(db.Boolean)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    token = db.Column(db.Text)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)
    registration_email_token = db.Column(db.Text)

    @orm.reconstructor
    def init_on_load(self):
        self.internal_id = None

    def __init__(self, input_parameters):
        self.is_removed = False
        self.is_email_approved = False
        self.registration_email_token = TokenSerializer.generate_auth_token(self.user_id)

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
        value = new_value.get(Constants.k_email)
        if value is not None:
            self.email = value

        value = new_value.get(Constants.k_last_name)
        if value is not None:
            self.last_name = value

        value = new_value.get(Constants.k_password)
        if value is not None:
            encrypted_password = passlib.encrypt(value, salt_length=100)
            self.password = encrypted_password

        value = new_value.get(Constants.k_first_name)
        if value is not None:
            self.first_name = value

        value = new_value.get(Constants.k_is_removed)
        if value is not None:
            self.is_removed = value
        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {Constants.k_user_id: self.user_id,
                       Constants.k_first_name: self.first_name,
                       Constants.k_last_name: self.last_name,
                       Constants.k_email: self.email,

                       Constants.k_is_removed: self.is_removed
                       }

        if self.time_stamp is not None:
            json_object[Constants.k_time_stamp] = self.time_stamp.isoformat()

        return json_object

    @staticmethod
    def find(email):
        items = User.query.filter_by(email=email).all()
        return items[0]
