from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    from db import db_init
    db_init()

    from api import tag,note,user
    app.register_blueprint(tag.tag)
    app.register_blueprint(note.note)
    app.register_blueprint(user.user)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)