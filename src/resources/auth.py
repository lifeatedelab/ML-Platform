from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.UserModel import UserModel, OAuthModel
from src.extensions import db
from flask_login import login_user, logout_user, current_user

from sqlalchemy.orm.exc import NoResultFound

# OAuth Library
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error


auth = Blueprint('auth', __name__)


google_login = make_google_blueprint(
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(OAuthModel, db.session, user=current_user),
)


@oauth_authorized.connect_via(google_login)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in.", category="error")
        return redirect(url_for('auth.login'))

    resp = blueprint.session.get("/oauth2/v1/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return redirect(url_for('auth.login'))

    info = resp.json()
    user_id = info["id"]

    query = OAuthModel.query.filter_by(
        provider=blueprint.name, provider_user_id=user_id)
    try:
        oauth = query.one()
        print('ini try')
    except NoResultFound:
        print('ini gagal')
        oauth = OAuthModel(provider=blueprint.name,
                           provider_user_id=user_id, token=token)

    full_name = info["name"]
    picture = info["picture"]
    email = info["email"]

    if oauth.user:
        login_user(oauth.user, remember=True)
    else:
        user = UserModel(email=email, name=full_name, picture=picture)
        oauth.user = user

        db.session.add_all([user, oauth])
        db.session.commit()

        login_user(user, remember=True)

    return redirect(url_for('main.dashboard'))


# notify error
@oauth_error.connect_via(google_login)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")


@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = UserModel.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Login Unsuccessful! Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.dashboard'))


@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = UserModel.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = UserModel(email=email, name=name,
                         password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
