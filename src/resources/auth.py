from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from sqlalchemy.orm.exc import NoResultFound

# OAuth Library
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error

from ..models.UserModel import UserModel, OAuthModel
from src.extensions import db
from src.util import send_reset_email

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

    first_name = info["given_name"]
    last_name = info["family_name"]
    # full_name = info["name"]
    picture = info["picture"]
    email = info["email"]

    if oauth.user:
        login_user(oauth.user, remember=True)
    else:
        user = UserModel(email=email, first_name=first_name,
                         last_name=last_name, picture=picture)
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
    # remember = True if request.form.get('remember') else False

    user = UserModel.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Login Unsuccessful! Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=True)
    return redirect(url_for('main.dashboard'))


@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    gender = request.form.get('gender')

    user = UserModel.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = UserModel(email=email, first_name=first_name, last_name=last_name, gender=gender,
                         password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        user = UserModel.query.filter_by(email=email).first()
        if user == None:
            flash('email not found', category='error')
            return redirect(url_for('auth.reset_request'))

        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    else:
        return render_template('auth/forgot_password.html')


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    user = UserModel.verify_reset_token(token)
    if request.method == 'GET':
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('auth.reset_request'))
        return render_template('auth/reset_password.html', token=token)

    if request.method == 'POST':
        password = request.form.get('password')

        hashed_password = generate_password_hash(
            password, method='sha256')

        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
