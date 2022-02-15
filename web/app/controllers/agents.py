from app import db
from app.models.agent import Agent


def create_agent(name, description, is_active):
    try:
        agent = Agent(name=name, description=description, is_active=is_active)
        db.session.add(agent)
        db.session.commit()
        return agent
    except Exception as e:
        print(str(e))
    return None


def get_all_agents():
    try:
        query = "SELECT * FROM agents;"
        return db.engine.execute(query).all()
    except Exception as e:
        print(str(e))


def get_agent_by_id(id):
    try:
        return Agent.query.filter_by(id=id).first()
    except Exception as e:
        print(str(e))
    return None


def get_agent_by_auth_code(auth_code):
    try:
        return Agent.query.filter_by(auth_code=auth_code).first()
    except Exception as e:
        print(str(e))
    return None