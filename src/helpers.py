
import os
import time

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
