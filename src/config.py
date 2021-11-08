from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

basepath = Path()
BASE = str(basepath.cwd())

# Load the environment variables
envars = basepath.cwd() / '.env'
load_dotenv(envars)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS')
    # UPLOAD_PATH = basedir + '/static'
    UPLOAD_AVATAR_EXTENSIONS = ['.jpg', '.png', '.jpeg']

    # OAUTHLIB_RELAX_TOKEN_SCOPE = True
    # OAUTHLIB_INSECURE_TRANSPORT = True
    # OAUTHLIB_RELAX_TOKEN_SCOPE = True
    OAUTHLIB_RELAX_TOKEN_SCOPE = os.getenv("OAUTHLIB_RELAX_TOKEN_SCOPE")
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    OAUTHLIB_INSECURE_TRANSPORT = os.getenv("OAUTHLIB_INSECURE_TRANSPORT")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "dev.db")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "dev.db")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "dev.db")


env_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
