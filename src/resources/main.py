from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from src.extensions import db, save_avatar_file, remove_file_avatar
from ..models.UserModel import OAuthModel, UserModel
import os

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html', name=current_user.name)


@main.route('/profile')
@login_required
def profile():
    google_acc = OAuthModel.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', google_acc=google_acc)


@main.route('/profile/update-profile')
@login_required
def update_profile():
    return render_template('update_profile.html')


@main.route('/profile/update-profile/post', methods=['POST'])
@login_required
def post_update_profile():
    user = UserModel.query.get(current_user.id)
    email = request.form.get('email')
    name = request.form.get('name')

    #
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]

        if file_ext not in current_app.config['UPLOAD_AVATAR_EXTENSIONS']:
            flash('JPG, JPEG, PNG', category='error')
            return redirect(url_for('main.update_profile'))

        avatar_name = str(current_user.id) + current_user.name + file_ext

        remove_file_avatar(user.picture)

        user.picture = avatar_name
        uploaded_file.save(save_avatar_file(avatar_name))
    #

    try:
        user.email = email
        user.name = name
        db.session.commit()
    except:
        return '<h1>ERROR</h1>'

    return redirect(url_for('main.profile'))
