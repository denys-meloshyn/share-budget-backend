from datetime import datetime

from shared_objects import db


class BudgetLimit(db.Model):
    __tablename__ = 'BUDGET_LIMIT'

    budget_limit_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))
    limit = db.Column(db.Double)
    date = db.Column(db.DateTime)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    def __init__(self, input_parameters):
        self.is_removed = False
        self.time_stamp = datetime.utcnow()