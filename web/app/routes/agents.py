from flask import Blueprint, jsonify, send_from_directory ,redirect, url_for, render_template, request, flash
from app.controllers.auth import login_required, admin_required
from app.controllers.agents import get_all_agents, create_agent
from app.controllers.files import get_file_by_id
from app.config import SecurityConfig

agents = Blueprint('agents', __name__)


@agents.get("/updates/download/<string:implant_id>")
def deliver(implant_id):
    download_path = SecurityConfig.ADMIN_UPLOADS
    try:
        implant = get_file_by_id(implant_id)
        if implant:
            return send_from_directory(download_path, implant.name), 200
        else:
            return jsonify({"error": "no_file"}), 404
    except Exception as e:
        print(str(e))


@agents.route("/dashboard/agents", methods=["GET", "POST"])
@login_required
@admin_required
def index():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if name is None or name == "":
            flash("No agent", "error")
            return redirect(url_for("agents.index"))
        if create_agent(name, description, True):
            return redirect(url_for("agents.index"))
        else:
            flash("Failed to save", "error")
    else:
        try:
            agents = get_all_agents()
            return render_template("dashboard/agents.html", agents=agents)
        except Exception as e:
            print(str(e))
