from flask import Flask
import bcrypt
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

# create and configure the app
app = Flask(__name__, instance_relative_config=True)

from db import db_init,get_db
db_init()

from api import tag,note,user
app.register_blueprint(tag.tag)
app.register_blueprint(note.note)
app.register_blueprint(user.user)

from models import User


if __name__ == '__main__':
    app.run(debug=True)