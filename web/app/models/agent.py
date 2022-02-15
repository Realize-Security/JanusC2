from app import db
import uuid


class Agent(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.String(36), primary_key=True)
    auth_code = db.Column(db.String(36), nullable=False)
    name = db.Column(db.String(36), nullable=False)
    description = db.Column(db.String(264), default="None")
    is_active = db.Column(db.Boolean, default=True)


    def __init__(self, name, description, is_active):
        self.id = str(uuid.uuid4())
        self.auth_code = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.is_active = is_active


