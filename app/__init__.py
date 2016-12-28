from flask.ext.bootstrap import Bootstrap
from flask import Flask

bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)

    bootstrap.init_app(app)
    app.debug = True

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app