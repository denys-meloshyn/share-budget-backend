from flask import Blueprint
from flask_mail import Mail
from flask_passlib import Passlib
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

blueprint = Blueprint('api', __name__)
api = Api(blueprint)

mail = Mail()
db = SQLAlchemy()
passlib = Passlib()
