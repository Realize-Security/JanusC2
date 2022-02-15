from flask import Blueprint, send_from_directory, redirect, url_for
from flask_login.utils import current_user

core = Blueprint('core', __name__)


@core.get('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    else:
        return redirect(url_for('auth.login'))


@core.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(core.config["STATIC_FOLDER"], filename)
