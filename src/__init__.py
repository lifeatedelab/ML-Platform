import os

from flask import Flask
from src.config import env_config
from .models.UserModel import login_manager
from .helpers import static_dir, template_dir


def create_app(config_name):
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # template_dir = os.path.join(basedir, 'templates')
    # static_dir = os.path.join(basedir, 'static')

    app = Flask(__name__, template_folder=template_dir,
                static_folder=static_dir)
    app.config.from_object(env_config[config_name])

    from src.extensions import db

    db.init_app(app)

    login_manager.init_app(app)

    from .models.UserModel import UserModel

    with app.app_context():
        db.create_all()

    # blueprint auth
    from .resources.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint google auth
    from .resources.auth import google_login
    app.register_blueprint(google_login, url_prefix="/login-google")

    # blueprint
    from .resources.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
