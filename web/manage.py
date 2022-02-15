from flask.cli import FlaskGroup

from app import app, db
from app.models.user import User
import app.models.command
import app.models.file
import app.models.agent_file
import app.models.agent

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("drop_db")
def drop_db():
    db.drop_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(
        email="mail@email.com",
        username="admin",
        password="C!#+haperoneAttendantUnderpayParachuteEpidermisSubtotal",
        is_admin=True,
        is_active=True
    ))
    db.session.commit()


if __name__ == "__main__":
    cli()
