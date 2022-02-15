from flask import abort, session, request
from functools import wraps

from app.models.agent import Agent


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if 'id' not in session:
            abort(401)
        return func(*args, **kwargs)

    return decorated_view


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if 'is_admin' not in session:
            abort(401)
        if session['is_admin'] != 1 or not session['is_admin']:
            abort(401)
        return func(*args, **kwargs)

    return decorated_view


def valid_agent(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            agent_auth = request.headers.get('Authorization')
            agent = Agent.query.filter_by(auth_code=agent_auth).first()
            if not agent and 'is_admin' not in session:
                abort(401)
        except Exception as e:
            print(str(e))
        return func(*args, **kwargs)

    return decorated_view