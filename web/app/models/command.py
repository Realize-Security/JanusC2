from datetime import datetime
import pytz
from app import db
import uuid
from app.config import DBConfig


def create_date():
    return datetime.now(pytz.timezone('UTC'))


class Command(db.Model):
    __tablename__ = 'commands'

    id = db.Column(db.String(36), primary_key=True)
    command = db.Column(db.String(600), nullable=True)
    content = db.Column(db.String(DBConfig.RESULT_MAX))
    created = db.Column(db.DateTime)
    time_received = db.Column(db.DateTime)

    agent = db.relationship('Agent')
    agent_id = db.Column(db.String(36), db.ForeignKey('agents.id'), nullable=False)

    def __init__(self, command, agent_id, content=None):
        self.id = str(uuid.uuid4())
        self.command = command
        self.content = content
        self.agent_id = agent_id
        self.created = create_date()
        self.time_received = create_date()
