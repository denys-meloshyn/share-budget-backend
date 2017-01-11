from sqlalchemy import orm
from datetime import datetime

from shared_objects import db
from constants import Constants


class Group(db.Model):
    __tablename__ = 'GROUP'

    group_id = db.Column(db.Integer, primary_key=True)
    modified_user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    name = db.Column(db.Text)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    @orm.reconstructor
    def init_on_load(self):
        self.internal_id = None

    def __init__(self, input_parameters):
        self.internal_id = None
        self.is_removed = False

        self.update(input_parameters)

    def update(self, new_value):
        value = new_value.get(Constants.k_user_id)
        if value is not None:
            self.modified_user_id = value

        value = new_value.get(Constants.k_name)
        if value is not None:
            self.name = value

        value = new_value.get(Constants.k_is_removed)
        if value is not None:
            self.is_removed = value

        value = new_value.get(Constants.k_internal_id)
        if value is not None:
            self.internal_id = value

        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {Constants.k_group_id: self.group_id,
                       Constants.k_name: self.name,

                       Constants.k_modified_user_id: self.modified_user_id,
                       Constants.k_is_removed: self.is_removed
                       }

        if self.internal_id is not None:
            json_object[Constants.k_internal_id] = self.internal_id

        if self.time_stamp is not None:
            json_object[Constants.k_time_stamp] = self.time_stamp.isoformat()

        return json_object
