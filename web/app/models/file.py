from app import db
import uuid


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(600), nullable=True)
    path = db.Column(db.String(600), nullable=True, default="")


    def __init__(self, name, path):
        self.id = str(uuid.uuid4())
        self.name = name
        self.path = path



