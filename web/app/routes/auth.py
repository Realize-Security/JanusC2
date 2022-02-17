from flask import Blueprint, render_template, redirect, url_for, flash, session, request
import itertools
from app.controllers.users import (
    get_user_by_email,
    # create_user,
    parse_user_object,
    logout_user,
    validate_email, 
    validate_username,
    validate_password
)
from app.controllers.auth import login_required
from app.config import SecurityConfig


auth = Blueprint('auth', __name__)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            if not SecurityConfig.REGISTRATION:
                flash("Registration closed", 'error')
                return redirect(url_for('auth.login'))
            else:
                user = parse_user_object(request.form)
                if len(user) < 4:
                    flash("Missing parameters", "error")
                    return redirect(url_for("auth.register"))
                username = user['username']
                email = user['email']
                password1 = user['password1']
                password2 = user['password2']
                reg_errs = list(itertools.chain(
                    validate_username(username),
                    validate_email(email),
                    validate_password(password1, password2)
                ))
                if len(reg_errs) > 0:
                    for e in reg_errs:
                        flash(e, "error")
                    return redirect(url_for("auth.register"))
                # if create_user(email, username, password1):
                #     flash('Registered successfully', 'success')
                #     return redirect(url_for('auth.login'))
                # else:
                #     flash("reg_errs", 'error')
                #     return redirect(url_for('auth.register'))
        except Exception as e:
            flash('Something went wrong.', 'error')
            print(str(e))
            return redirect(url_for('auth.register'))
    else:
        return render_template("auth/register.html")


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            user = get_user_by_email(email)

            if user.check_password(password) and user is not None:
                session['id'] = user.id
                session['username'] = user.username
                session['is_admin'] = user.is_admin
                next = request.args.get('next')
                if next is None or not next[0] == '/':
                    next = url_for('dashboard.index')
                return redirect(next)
        except Exception as e:
            print(str(e))
    else:
        return render_template("auth/login.html")

    return render_template("auth/login.html")


@auth.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user(session)
    return redirect(url_for('auth.login'))
