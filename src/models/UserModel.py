from flask_login import UserMixin, LoginManager
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from src.extensions import db
import os


class UserModel(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    picture = db.Column(db.String(1000))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(os.getenv('SECRET_KEY'), expires_sec)
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(os.getenv('SECRET_KEY'))
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return UserModel.query.get(user_id)

    # def __repr__(self):
    #     return f"User('{self.email}', '{self.picture}')"


class OAuthModel(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    user = db.relationship(UserModel)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))
