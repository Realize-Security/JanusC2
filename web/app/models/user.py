from app import db, login_manager
from flask_login import UserMixin
from flask_bcrypt import check_password_hash, generate_password_hash
import uuid


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, email, password, is_admin, is_active):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = self.hash_password(password)
        self.is_admin = is_admin
        self.is_active = is_active

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod  # TODO: Can this be removed?
    def hash_password(password):
        return generate_password_hash(password).decode('utf-8')
