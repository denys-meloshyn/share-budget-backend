from datetime import datetime

from shared_objects import db


class Group(db.Model):
    __tablename__ = 'GROUP'
    k_group_id = 'group_id'
    k_modified_user_id = 'modified_user_id'
    k_name = 'name'

    group_id = db.Column(db.Integer, primary_key=True)
    modified_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    budget_limit_id = db.Column(db.Integer, db.ForeignKey('budget_limit.budget_limit_id'))
    name = db.Column(db.Text)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    def __init__(self, input_parameters):
        self.is_removed = False
        self.time_stamp = datetime.utcnow()