from flask import jsonify, session
from app import db
from app.models.user import User
from app.config import SecurityConfig
import re


def create_user(email, username, password):
    try:
        user = User(username, email, password, is_admin=False, is_active=False)
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        print(str(e))
    return None


def update_user(user_updates):
    try:
        if 'password1' in user_updates:
            p1 = user_updates['password1']
            p2 = user_updates['password2']
            pass_errors = validate_password(p1, p2)
            if len(pass_errors) == 0:
                user_updates.pop('password1')
                user_updates.pop('password2')
                user_updates['password'] = User.hash_password(p1)
            else:
                return None, pass_errors

        if 'username' in user_updates:
            user_errs = validate_username(user_updates['username'])
            if len(user_errs) > 0:
                return None, user_errs

        user = User.query.filter_by(id=session['id']).first()
        user_updates.pop('id')
        for el in user_updates:
            setattr(user, el, user_updates[el])

        db.session.commit()
        return True, user
    except Exception as e:
        print(str(e))
    return None, None


def get_user_by_email(email):
    try:
        return User.query.filter_by(email=email).first()
    except Exception as e:
        print(str(e))


def get_user_by_id(userid):
    try:
        return User.query.filter_by(id=userid).first()
    except Exception as e:
        print(str(e))


def get_user_by_username(username):
    try:
        return User.query.filter_by(username=username).first()
    except Exception as e:
        print(str(e))


def get_all_users():
    try:
        return db.engine.execute("SELECT email, username, is_admin, is_active FROM users;")
    except Exception as e:
        print(str(e))
    return None


def logout_user(session):
    if 'id' in session:
        session.pop('id')


def is_authenticated(session):
    return 'id' in session


def validate_email(email):
    errs = []
    if get_user_by_email(email):
        errs.append("User already exists")
    return errs


def validate_username(username):
    errs = []
    if re.match("[a-zA-Z0-9]{3,15}", username) is None:
        errs.append("Username must be between 3 and 15 characters long and contain no special characters")
    return errs


def validate_password(pass1, pass2):
    errs = []
    pass_min = SecurityConfig.PASSWORD_MIN_LENGTH
    if pass1 != pass2:
        errs.append("Passwords not equal")
    if len(pass1) < pass_min:
        errs.append("Password minimum length is " + str(pass_min))
    return errs


def parse_user_object(form):
    new_user = {}
    try:
        user = {
            "username": form.get('username'),
            "email": form.get('email'),
            "password1": form.get('password_1'),
            "password2": form.get('password_2'),
        }

        for el in user:
            if user[el] and user[el] != '':
                new_user[el] = user[el]

        return new_user

    except Exception as e:
        print(str(e))


def all_users_to_json():
    users = get_all_users()
    json = {}
    for user in users:
        tmp_json = user_to_dict(user)
        json[user.email] = tmp_json
    return jsonify(json)


def user_to_json(user):
    return jsonify(user_to_dict(user))


def user_to_dict(user):
    return dict(
        username=user.username,
        email=user.email,
        is_admin=user.is_admin
    )
