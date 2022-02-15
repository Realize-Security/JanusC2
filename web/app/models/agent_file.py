from app import db
import uuid

class AgentFile(db.Model):
    __tablename__ = 'agent_files'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(600), nullable=True)
    path = db.Column(db.String(600), nullable=True, default="")

    agent = db.relationship('Agent')
    agent_id = db.Column(db.String(36), db.ForeignKey('agents.id'))


    def __init__(self, name, agent_id, path):
        self.id = str(uuid.uuid4())
        self.name = name
        self.agent_id = agent_id
        self.path = path

