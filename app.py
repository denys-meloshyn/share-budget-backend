from apis.api_v1 import namespace as namespace_1
from application import api, flask_app, blueprint
from model import db

api.add_namespace(namespace_1)
flask_app.register_blueprint(blueprint)

if __name__ == '__main__':
    db.create_all()
    flask_app.run(debug=True)
