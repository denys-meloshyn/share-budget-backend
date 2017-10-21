from datetime import datetime

from sqlalchemy import orm

from utility.constants import Constants
from utility.shared_objects import db


class CategoryLimit(db.Model):
    __tablename__ = 'CATEGORY_LIMIT'

    category_limit_id = db.Column(db.Integer, primary_key=True)
    modified_user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('CATEGORY.category_id'))
    limit = db.Column(db.Float)
    date = db.Column(db.Date)
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
        value = new_value.get(Constants.JSON.category_id)
        if value is not None:
            self.category_id = value

        value = new_value.get(Constants.JSON.limit)
        if value is not None:
            self.limit = value

        value = new_value.get(Constants.JSON.date)
        if value is not None:
            self.date = value.replace(day=1)

        value = new_value.get(Constants.JSON.is_removed)
        if value is not None:
            self.is_removed = value

        value = new_value.get(Constants.JSON.internal_id)
        if value is not None:
            self.internal_id = value

        value = new_value.get(Constants.JSON.user_id)
        if value is not None:
            self.modified_user_id = value

        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {Constants.JSON.category_limit_id: self.category_limit_id,
                       Constants.JSON.category_id: self.category_id,
                       Constants.JSON.limit: self.limit,

                       Constants.JSON.modified_user_id: self.modified_user_id,
                       Constants.JSON.is_removed: self.is_removed
                       }

        if self.internal_id is not None:
            json_object[Constants.JSON.internal_id] = self.internal_id

        if self.date is not None:
            json_object[Constants.JSON.date] = self.date.strftime(Constants.JSON.date_format)

        if self.time_stamp is not None:
            json_object[Constants.JSON.time_stamp] = self.time_stamp.isoformat()

        return json_object
