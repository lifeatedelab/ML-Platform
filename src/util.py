
import os
import time

from flask import url_for

from flask_mail import Message
from src.extensions import mail


basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basedir, 'templates')
static_dir = os.path.join(basedir, 'static')
avatar_upload_dir = os.path.join(static_dir, 'images/avatar')
timestr = time.strftime("%Y%m%d%H%M%S")


def save_avatar_file(avatar_name):
    # file_ext = os.path.splitext(filename)[1]
    return os.path.join(avatar_upload_dir, avatar_name)


def is_path_exist(filename):
    if os.path.exists(os.path.join(avatar_upload_dir, filename)):
        return True
    else:
        return False


def remove_file_avatar(filename):
    if is_path_exist(filename):
        os.remove(os.path.join(avatar_upload_dir, filename))


def mail_body_forgot_pass(user, token):
    return f"""
    <div>
        <p>Hi, {user.name}!</p>
        <p>To reset your password, visit the following link:</p>
        <a
        href="{url_for('auth.reset_token', token=token, _external=True)}"
        style="
            background-color: rgb(15, 146, 233);
            color: #ffffff;
            padding: 0.8rem 5rem;
            border-radius: 4px;
            font-size: 14px;
            font-weight: bold;
            text-decoration: none;
        "
        >Reset Password</a
        >
        <p>
        <br />
        <b>
            If you did not make this request then simply ignore this email and no
            changes will be made.
        </b>
        </p>
    </div>
    """


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])

    msg.html = mail_body_forgot_pass(user, token)
    mail.send(msg)
