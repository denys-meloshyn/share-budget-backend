from application import create_app
from model import db

flask_app = create_app()
flask_app.app_context().push()
db.create_all()
db.session.commit()

if __name__ == '__main__':
    flask_app.run(debug=True)
