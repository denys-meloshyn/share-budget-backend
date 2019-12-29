from datetime import datetime

from model import db
from utility.constants import Constants


class UserGroup(db.Model):
    __tablename__ = 'USER_GROUP'

    user_group_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('GROUP.group_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    @staticmethod
    def is_user_part_of_group(user_id, group_id):
        user_group = UserGroup.query.filter(
            db.and_(UserGroup.group_id == group_id, UserGroup.user_id == user_id, UserGroup.is_removed.is_(False))
        ).first()

        if user_group is None:
            return False

        return True

    def __init__(self, input_parameters):
        self.internal_id = None
        self.is_removed = False

        self.update(input_parameters)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False

        if self.user_group_id != other.user_group_id:
            return False

        if self.user_id != other.user_id:
            return False

        if self.group_id != other.group_id:
            return False

        if self.is_removed != other.is_removed:
            return False

        return True

    def __repr__(self):
        return '(user_group_id={}, user_id={}, group_id={}, is_removed={})'.format(self.user_group_id,
                                                                                   self.user_id,
                                                                                   self.group_id,
                                                                                   self.is_removed)

    def update(self, new_value):
        value = new_value.get(Constants.JSON.user_group_id)
        if value is not None:
            self.user_group_id = value

        value = new_value.get(Constants.JSON.user_id)
        if value is not None:
            self.user_id = value

        value = new_value.get(Constants.JSON.group_id)
        if value is not None:
            self.group_id = value

        value = new_value.get(Constants.JSON.is_removed)
        if value is not None:
            self.is_removed = value

        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {Constants.JSON.user_group_id: self.user_group_id,
                       Constants.JSON.user_id: self.user_id,
                       Constants.JSON.group_id: self.group_id,

                       Constants.JSON.is_removed: self.is_removed
                       }

        if self.time_stamp is not None:
            json_object[Constants.JSON.time_stamp] = self.time_stamp.isoformat()

        return json_object
