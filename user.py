from datetime import datetime
from constants import Constants
from shared_objects import db


class User(db.Model):
    __tablename__ = 'user'

    k_first_name = 'firstName'
    k_last_name = 'lastName'
    k_email = 'email'
    k_token = 'token'

    user_id = db.Column(db.Integer, primary_key=True)
    is_email_approved = db.Column(db.Boolean)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    token = db.Column(db.Text)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    def __init__(self):
        pass

    def __init__(self, input_parameters):
        self.is_removed = False
        self.is_email_approved = False
        self.time_stamp = datetime.utcnow()

        self.email = input_parameters.get(self.k_email)
        self.last_name = input_parameters.get(self.k_last_name)
        self.first_name = input_parameters.get(self.k_first_name)

    def to_dict(self):
        json_object = {Constants.k_user_id: self.user_id,
                       self.k_first_name: self.first_name,
                       self.k_last_name: self.last_name,
                       self.k_email: self.email,
                       }

        return json_object
