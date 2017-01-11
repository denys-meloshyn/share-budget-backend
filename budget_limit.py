from datetime import datetime

from sqlalchemy import orm
from shared_objects import db
from constants import Constants


class BudgetLimit(db.Model):
    __tablename__ = 'BUDGET_LIMIT'

    budget_limit_id = db.Column(db.Integer, primary_key=True)
    modified_user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('GROUP.group_id'))
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
        value = new_value.get(Constants.k_user_id)
        if value is not None:
            self.modified_user_id = value

        value = new_value.get(Constants.k_group_id)
        if value is not None:
            self.group_id = value

        value = new_value.get(Constants.k_limit)
        if value is not None:
            self.limit = value

        value = new_value.get(Constants.k_date)
        if value is not None:
            self.date = value.replace(day=1)

        value = new_value.get(Constants.k_internal_id)
        if value is not None:
            self.internal_id = value

        value = new_value.get(Constants.k_is_removed)
        if value is not None:
            self.is_removed = value
        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {Constants.k_budget_limit_id: self.budget_limit_id,
                       Constants.k_group_id: self.group_id,
                       Constants.k_limit: self.limit,

                       Constants.k_modified_user_id: self.modified_user_id,
                       Constants.k_is_removed: self.is_removed
                       }

        if self.internal_id is not None:
            json_object[Constants.k_internal_id] = self.internal_id

        if self.date is not None:
            json_object[Constants.k_date] = self.date.strftime(Constants.k_date_format)

        if self.time_stamp is not None:
            json_object[Constants.k_time_stamp] = self.time_stamp.isoformat()

        return json_object
