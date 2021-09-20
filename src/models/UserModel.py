from flask_login import UserMixin
from src.extensions import db


class UserModel(UserMixin, db.Model):
    __tablename__ = "users"
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
