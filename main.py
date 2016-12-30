import os
from shared_objects import SharedObjects

os.environ.setdefault("DATABASE_URL", "postgresql://localhost/postgres")

if __name__ == '__main__':
    SharedObjects.instance().flask_app.run(debug=True)
