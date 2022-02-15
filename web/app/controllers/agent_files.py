from app.models.agent_file import AgentFile
from app import db
import os

# TODO: Refactor repetetive code

def get_all_agent_files():
    try:
        files = AgentFile.query.all()
        return files
    except Exception as e:
        print(str(e))
    return None


def agent_file_by_id(id, agent_id):
    try:
        file = AgentFile.query.filter_by(id=id, agent_id=agent_id).first()
        return file
    except Exception as e:
        print(str(e))
    return None


def save_agent_file(file, path, filename, agent_id):
    try:
        fullpath = os.path.join(path, filename)
        file.save(fullpath)
        f = AgentFile(name=filename, path=fullpath, agent_id=agent_id)
        db.session.add(f)
        db.session.commit()
    except Exception as e:
        print(str(e))


def delete_agent_file(id):
    try:
        file = AgentFile.query.filter_by(id=id).first()
        path = file.path
        db.session.delete(file)
        db.session.commit()
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(str(e))