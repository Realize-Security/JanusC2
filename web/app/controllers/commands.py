from app import db
from app.models.command import Command
from sqlalchemy.sql import text


def create_command(command, agent_id):
    try:
        cmd = Command(command=command, agent_id=agent_id)
        db.session.add(cmd)
        db.session.commit()
        return cmd
    except Exception as e:
        print(str(e))
    return None


def update_response(cmd_id, response, agent_id):
    try:
        cmd = Command.query.filter_by(id=cmd_id, agent_id=agent_id).first()
        cmd.content = response
        db.session.commit()
        return True
    except Exception as e:
        print(str(e))
    return None


def get_unfulfilled(agent_id):
    try:
        return Command.query.filter_by(content=None, agent_id=agent_id).all()
    except Exception as e:
        print(str(e))


def cancel(cmd_id):
    try:
        cmd = Command.query.filter_by(content=None, id=cmd_id).first()
        cmd.content = "CANCELLED"
        db.session.commit()
        return True
    except Exception as e:
        print(str(e))
    return None


def get_one_cmd_by_id(id, agent_id):
    try:
        cmd = Command.query.filter_by(id=id, agent_id=agent_id).first()
        return cmd
    except Exception as e:
        print(str(e))


def get_agent_by_cmd(id):
    try:
        cmd = Command.query.filter_by(id=id).first()
        return cmd
    except Exception as e:
        print(str(e))


def get_all_cmds_by_id(agent_id):
    try:
        query = text("SELECT * FROM commands WHERE agent_id = :agent_id ORDER BY created DESC;")
        return db.engine.execute(query, agent_id=agent_id).all()
    except Exception as e:
        print(str(e))
    return None

