import os
import redis


class AppConfig(object):
    """Parent configuration class."""
    basedir = os.path.abspath(os.path.dirname(__file__))
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Cookie settings
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url('redis://redis:6379')
    SESSION_COOKIE_NAME = "janus"
    SESSION_COOKIE_PATH = "/"
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Strict"
    #
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = os.getenv('FLASK_DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    LOG_ENABLED = os.getenv('LOG_ENABLED')
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/static"
    #


class SecurityConfig(object):
    """Security specific strings and configs"""
    PASSWORD_MIN_LENGTH = 10
    REGISTRATION_ERROR = 'Please check your details and try again'
    REGISTRATION = False
    INIT_ATTACK = True
    USER_UPLOADS = "/vol/uploads/"
    ADMIN_UPLOADS = "/vol/admin/uploads/"


class LogConf(object):
    """Logging config strings"""
    LOGPATH = "/vol/log"
    LOGFILE = "flask.log"
    DEBUG = "debug"
    INFO = "info"
    WARN = "warning"
    ERROR = "error"
    CRIT = "critical"
