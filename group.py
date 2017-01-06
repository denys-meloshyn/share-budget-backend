from datetime import datetime

from shared_objects import db
from constants import Constants


class Group(db.Model):
    __tablename__ = 'GROUP'
    k_group_id = 'groupId'
    k_modified_user_id = 'modifiedUserId'
    k_name = 'name'

    group_id = db.Column(db.Integer, primary_key=True)
    modified_user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    name = db.Column(db.Text)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    def __init__(self, input_parameters):
        self.is_removed = False

        self.update(input_parameters)

    def update(self, new_value):
        value = new_value.get(Constants.k_user_id)
        if value is not None:
            self.modified_user_id = value

        value = new_value.get(self.k_name)
        if value is not None:
            self.name = value

        value = new_value.get(Constants.k_is_removed)
        if value is not None:
            self.is_removed = value
        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {self.k_group_id: self.group_id,
                       self.k_modified_user_id: self.modified_user_id,
                       self.k_name: self.name,

                       Constants.k_is_removed: self.is_removed
                       }

        if self.time_stamp is not None:
            json_object[Constants.k_time_stamp] = self.time_stamp.isoformat()

        return json_object