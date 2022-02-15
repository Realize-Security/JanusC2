from flask import Blueprint, redirect, url_for, render_template, request, flash
from app.controllers.auth import login_required, admin_required
from app.controllers.agents import get_all_agents, create_agent

agents = Blueprint('agents', __name__)


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



