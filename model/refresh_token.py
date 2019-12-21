from datetime import datetime

from model import db


class RefreshToken(db.Model):
    __tablename__ = 'REFRESH_TOKEN'

    refresh_token = db.Column(db.Text, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    time_stamp = db.Column(db.DateTime)

    def __init__(self, refresh_token, user_id):
        self.user_id = user_id
        self.refresh_token = refresh_token
        self.time_stamp = datetime.utcnow()

    @staticmethod
    def find(refresh_token):
        return RefreshToken.query.filter_by(refresh_token=refresh_token).first()
