from datetime import datetime

from group import Group
from shared_objects import db
from constants import Constants


class BudgetLimit(db.Model):
    __tablename__ = 'BUDGET_LIMIT'
    k_date = 'date'
    k_limit = 'limit'
    k_budget_limit_id = 'budget_limit_id'

    budget_limit_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('GROUP.group_id'))
    limit = db.Column(db.Float)
    date = db.Column(db.Date)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    def __init__(self, input_parameters):
        self.is_removed = False

        self.update(input_parameters)

    def update(self, new_value):
        value = new_value.get(Group.k_group_id)
        if value is not None:
            self.group_id = value

        value = new_value.get(self.k_limit)
        if value is not None:
            self.limit = value

        value = new_value.get(self.k_date)
        if value is not None:
            self.date = value.replace(day=1)

        value = new_value.get(Constants.k_is_removed)
        if value is not None:
            self.is_removed = value
        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {self.k_budget_limit_id: self.budget_limit_id,
                       Group.k_group_id: self.group_id,
                       self.k_limit: self.limit,

                       Constants.k_is_removed: self.is_removed
                       }

        if self.date is not None:
            json_object[self.k_date] = self.date.strftime('%Y-%m-%d')

        if self.time_stamp is not None:
            json_object[Constants.k_time_stamp] = self.time_stamp.isoformat()

        return json_object
