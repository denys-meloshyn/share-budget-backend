from datetime import datetime

from sqlalchemy import orm

from model import db
from utility.constants import Constants


class Expense(db.Model):
    __tablename__ = 'EXPENSE'

    expense_id = db.Column(db.Integer, primary_key=True)
    modified_user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('GROUP.group_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('CATEGORY.category_id'))
    name = db.Column(db.Text)
    price = db.Column(db.Float)
    creation_date = db.Column(db.DateTime)
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
        value = new_value.get(Constants.JSON.group_id)
        if value is not None:
            self.group_id = value

        value = new_value.get(Constants.JSON.name)
        if value is not None:
            self.name = value

        value = new_value.get(Constants.JSON.price)
        if value is not None:
            self.price = value

        value = new_value.get(Constants.JSON.is_removed)
        if value is not None:
            self.is_removed = value

        value = new_value.get(Constants.JSON.internal_id)
        if value is not None:
            self.internal_id = value

        value = new_value.get(Constants.JSON.user_id)
        if value is not None:
            self.modified_user_id = value

        value = new_value.get(Constants.JSON.creation_date)
        if type(value) is tuple:
            self.creation_date = value[0].replace(tzinfo=None)

        value = new_value.get(Constants.JSON.category_id)
        if type(value) is not None:
            self.category_id = value

        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {Constants.JSON.expense_id: self.expense_id,
                       Constants.JSON.group_id: self.group_id,
                       Constants.JSON.name: self.name,
                       Constants.JSON.price: self.price,
                       Constants.JSON.category_id: self.category_id,

                       Constants.JSON.modified_user_id: self.modified_user_id,
                       Constants.JSON.is_removed: self.is_removed
                       }

        if self.creation_date is not None:
            json_object[Constants.JSON.creation_date] = self.creation_date.isoformat()

        if self.internal_id is not None:
            json_object[Constants.JSON.internal_id] = self.internal_id

        if self.time_stamp is not None:
            json_object[Constants.JSON.time_stamp] = self.time_stamp.isoformat()

        return json_object
