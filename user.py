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

    def __init__(self, input_parameters):
        self.is_removed = False
        self.is_email_approved = False
        self.registration_email_token = TokenSerializer.generate_auth_token(self.user_id)

        self.update(input_parameters)

    def update(self, new_value):
        value = new_value.get(self.k_email)
        if value is not None:
            self.email = value

        value = new_value.get(self.k_last_name)
        if value is not None:
            self.last_name = value

        value = new_value.get(self.k_password)
        if value is not None:
            encrypted_password = passlib.encrypt(value, salt_length=100)
            self.password = encrypted_password

        value = new_value.get(self.k_first_name)
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
