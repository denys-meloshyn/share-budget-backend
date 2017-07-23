from flask_mail import Mail
from flask_passlib import Passlib
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api as SwaggerApi

mail = Mail()
db = SQLAlchemy()
passlib = Passlib()
swagger_app = SwaggerApi()
