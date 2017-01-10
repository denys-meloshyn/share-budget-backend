from datetime import datetime

from shared_objects import db
from constants import Constants


class UserGroup(db.Model):
    __tablename__ = 'USER_GROUP'

    user_group_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('GROUP.group_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    def __init__(self):
        self.is_removed = False
        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {Constants.k_user_id: self.user_id,
                       Constants.k_user_group_id: self.user_group_id,
                       Constants.k_group_id: self.group_id,

                       Constants.k_is_removed: self.is_removed
                       }

        if self.time_stamp is not None:
            json_object[Constants.k_time_stamp] = self.time_stamp.isoformat()

        return json_object
