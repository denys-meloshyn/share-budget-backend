from datetime import datetime

from sqlalchemy import orm

from shared_objects import db
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
        value = new_value.get(Constants.k_group_id)
        if value is not None:
            self.group_id = value

        value = new_value.get(Constants.k_name)
        if value is not None:
            self.name = value

        value = new_value.get(Constants.k_price)
        if value is not None:
            self.price = value

        value = new_value.get(Constants.k_is_removed)
        if value is not None:
            self.is_removed = value

        value = new_value.get(Constants.k_internal_id)
        if value is not None:
            self.internal_id = value

        value = new_value.get(Constants.k_user_id)
        if value is not None:
            self.modified_user_id = value

        value = new_value.get(Constants.k_creation_date)
        if type(value) is tuple:
            self.creation_date = value[0].replace(tzinfo=None)

        value = new_value.get(Constants.k_category_id)
        if type(value) is not None:
            self.category_id = value

        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {Constants.k_expense_id: self.expense_id,
                       Constants.k_group_id: self.group_id,
                       Constants.k_name: self.name,
                       Constants.k_price: self.price,
                       Constants.k_category_id: self.category_id,

                       Constants.k_modified_user_id: self.modified_user_id,
                       Constants.k_is_removed: self.is_removed
                       }

        if self.creation_date is not None:
            json_object[Constants.k_creation_date] = self.creation_date.isoformat()

        if self.internal_id is not None:
            json_object[Constants.k_internal_id] = self.internal_id

        if self.time_stamp is not None:
            json_object[Constants.k_time_stamp] = self.time_stamp.isoformat()

        return json_object
