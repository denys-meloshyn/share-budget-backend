import os

from flask import send_from_directory

from application import create_app
from model import db

flask_app = create_app()
flask_app.app_context().push()
db.create_all()
db.session.commit()


@flask_app.route('/.well-known/<path:path>')
def send_well_known(path):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, '.well-known'), path)


if __name__ == '__main__':
    flask_app.run(debug=True)
