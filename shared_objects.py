from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api as SwaggerApi

db = SQLAlchemy()
swagger_app = SwaggerApi()
