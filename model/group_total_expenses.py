from model import db
from utility.constants import Constants


class GroupTotalExpenses(db.Model):
    __tablename__ = 'GROUP_TOTAL_EXPENSES'

    group_total_expenses_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('GROUP.group_id'))
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    def __init__(self):
        self.is_removed = False

    def to_json(self):
        json_object = {
            Constants.JSON.group_id: self.group_id,
            Constants.JSON.is_removed: self.is_removed
        }

        if self.time_stamp is not None:
            json_object[Constants.JSON.time_stamp] = self.time_stamp.isoformat()

        return json_object
