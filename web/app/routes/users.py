from flask import Blueprint, render_template, session, request, flash
from app.controllers.users import (
    get_all_users,
    get_user_by_id,
    update_user,
    parse_user_object,
)
from app.controllers.auth import login_required, admin_required

users = Blueprint('users', __name__)


@users.route("/dashboard/users", methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    return render_template("dashboard/users.html", users=get_all_users())


@users.route("/dashboard/settings", methods=['GET', 'POST'])
@login_required
def settings():
    user = get_user_by_id(session['id'])
    if request.method == 'POST':
        try:
            user_updates = parse_user_object(request.form)
            user_updates['id'] = session['id']
            if len(user_updates) > 0:
                success, result = update_user(user_updates)
                if not success:
                    for err in result:
                        flash(err, 'error')
                    return render_template("dashboard/settings.html", user=user)
                else:
                    flash('Successfully updated', 'success')
                    return render_template("dashboard/settings.html", user=result)
            else:
                flash('Nothing to update', 'warn')
        except Exception as e:
            flash('Something went wrong.', 'error')
            print(str(e))
            return render_template("dashboard/settings.html", user=user)

    return render_template("dashboard/settings.html", user=user)
