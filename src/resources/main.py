from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db
from src.util import save_avatar_file, remove_file_avatar
from ..models.UserModel import OAuthModel, UserModel
import os

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    full_name = f"{current_user.first_name} {current_user.last_name}"
    return render_template('dashboard/dashboard.html', name=full_name)


@main.route('/profile')
@login_required
def profile():
    google_acc = OAuthModel.query.filter_by(user_id=current_user.id).first()
    print(google_acc)
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
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    gender = request.form.get('gender')
    jalan = request.form.get('jalan')
    kota = request.form.get('kota')
    provinsi = request.form.get('provinsi')

    # uploaded_file = request.files['file']
    # filename = secure_filename(uploaded_file.filename)
    # if filename != '':
    #     file_ext = os.path.splitext(filename)[1]

    #     if file_ext not in current_app.config['UPLOAD_AVATAR_EXTENSIONS']:
    #         flash('JPG, JPEG, PNG', category='error')
    #         return redirect(url_for('main.update_profile'))

    #     avatar_name = str(current_user.id) + current_user.name + file_ext

    #     remove_file_avatar(user.picture)

    #     user.picture = avatar_name
    #     uploaded_file.save(save_avatar_file(avatar_name))

    try:
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender
        user.jalan = jalan
        user.kota = kota
        user.provinsi = provinsi
        db.session.commit()
    except:
        flash('Error')
        return redirect(url_for('main.profile'))

    flash('Update Success!')
    return redirect(url_for('main.profile'))
