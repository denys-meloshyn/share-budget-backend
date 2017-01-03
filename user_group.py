from datetime import datetime

from user import User
from shared_objects import db
from constants import Constants


class UserGroup(db.Model):
    __tablename__ = 'USER_GROUP'

    k_user_group_id = 'user_group_id'

    user_group_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    def __init__(self, input_parameters):
        self.is_removed = False
        self.time_stamp = datetime.utcnow()