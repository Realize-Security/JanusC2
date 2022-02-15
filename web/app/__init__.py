from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
import traceback
import logging
import os
from time import strftime
from app.config import LogConf, AppConfig


app = Flask(__name__, static_url_path='/static')
app.config.from_object("app.config.AppConfig")
server_session = Session(app)


@app.errorhandler(401)
def page_not_found(e):
    if "/api" in request.path:
        return jsonify(error=401)
    else:
        return render_template('error/401.html'), 401


logger = logging.getLogger('werkzeug')
logpath = os.path.join(LogConf.LOGPATH, LogConf.LOGFILE)
handler = logging.FileHandler(logpath)
logger.addHandler(handler)

db = SQLAlchemy(app)
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect()
csrf.init_app(app)

from app.routes.core import core
from app.routes.auth import auth
from app.routes.dashboard import dashboard
from app.routes.commands import commands
from app.routes.users import users
from app.routes.files import files
from app.routes.agents import agents

if AppConfig.LOG_ENABLED:
    @app.after_request
    def after_request(response):
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme,
                     request.full_path, response.status)
        return response


    @app.errorhandler(Exception)
    def exceptions(e):
        tb = traceback.format_exc()
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method,
                     request.scheme, request.full_path, tb)
        return "Error was logged"

app.register_blueprint(core)
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(commands)
app.register_blueprint(users)
app.register_blueprint(files)
app.register_blueprint(agents)
