from datetime import datetime

from sqlalchemy import orm

from utility.constants import Constants
from utility.shared_objects import db


class Category(db.Model):
    __tablename__ = 'CATEGORY'

    category_id = db.Column(db.Integer, primary_key=True)
    modified_user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('GROUP.group_id'))
    name = db.Column(db.Text)
    is_removed = db.Column(db.Boolean, default=False)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow())

    @orm.reconstructor
    def init_on_load(self):
        self.internal_id = None

    def __init__(self, input_parameters):
        self.internal_id = None
        self.is_removed = False

        self.update(input_parameters)

    def update(self, new_value):
        value = new_value.get(Constants.JSON.group_id)
        if value is not None:
            self.group_id = value

        value = new_value.get(Constants.JSON.name)
        if value is not None:
            self.name = value

        value = new_value.get(Constants.JSON.is_removed)
        if value is not None:
            self.is_removed = value

        value = new_value.get(Constants.JSON.user_id)
        if value is not None:
            self.modified_user_id = value

        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {Constants.JSON.category_id: self.category_id,
                       Constants.JSON.group_id: self.group_id,
                       Constants.JSON.name: self.name,

                       Constants.JSON.modified_user_id: self.modified_user_id,
                       Constants.JSON.is_removed: self.is_removed
                       }

        if self.time_stamp is not None:
            json_object[Constants.JSON.time_stamp] = self.time_stamp.isoformat()

        return json_object
