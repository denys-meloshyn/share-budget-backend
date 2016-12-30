from shared_objects import SharedObjects
db = SharedObjects.instance().db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    is_email_approved = db.Column(db.Bool)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    token = db.Column(db.Text)
    time_stamp = db.Column(db.DateTime)
