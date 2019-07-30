from apis.api_v1 import namespace as namespace_1
from model import db
from utility.shared_objects import app, api, blueprint

api.add_namespace(namespace_1)
app.register_blueprint(blueprint)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
