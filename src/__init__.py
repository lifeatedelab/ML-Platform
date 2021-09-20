import os

from flask import Flask
from flask_login import LoginManager
from src.config import env_config


def create_app(config_name):
    basedir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(basedir, 'templates')

    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object(env_config[config_name])

    from src.extensions import db

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models.UserModel import UserModel

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    # blueprint auth
    from .resources.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint
    from .resources.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
