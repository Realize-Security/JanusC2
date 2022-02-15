from flask import Blueprint, render_template, request, redirect, url_for
from app.controllers.auth import login_required, admin_required
from app.controllers.files import save_file, delete_file, get_all_files
from app.controllers.agents import get_all_agents
from app.config import SecurityConfig
from app.controllers.agent_files import save_agent_file, get_all_agent_files, delete_agent_file

files = Blueprint('files', __name__)


@files.route("/dashboard/files", methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    return render_template(
        "dashboard/files.html",
        agent_files=get_all_agent_files(),
        files=get_all_files(),
        agents=get_all_agents()
    )


@files.route("/dashboard/files/upload", methods=['GET', 'POST'])
@login_required
@admin_required
def upload():
    # Agent ID blocking upload for admin users
    if request.method == 'POST':
        try:
            uploaded = request.files.getlist('file')
            agent_id = request.form.get('agent')
            path = SecurityConfig.ADMIN_UPLOADS
            for f in uploaded:
                if f.filename != '' and f.filename is not None:
                    if agent_id == 'None':
                        save_file(file=f, path=path, filename=f.filename) 
                    else:
                        save_agent_file(file=f, path=path, filename=f.filename, agent_id=agent_id)
            return redirect(url_for("files.index"))
        except Exception as e:
            print(str(e))
            return redirect(url_for("files.index"))
    else:
        return redirect(url_for("files.index"))



@files.route("/dashboard/files/delete/<string:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def delete(id):
    # Agent ID blocking upload for admin users
    if request.method == 'POST':
        try:
            if request.form.get('agent_file'):
                delete_agent_file(id)
            else:
                delete_file(id)
            return redirect(url_for("files.index"))
        except Exception as e:
            print(str(e))
            return redirect(url_for("files.index"))
    else:
        return redirect(url_for("files.index"))
