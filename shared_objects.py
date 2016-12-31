from flask_passlib import Passlib
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api as SwaggerApi

db = SQLAlchemy()
passlib = Passlib()
swagger_app = SwaggerApi()
