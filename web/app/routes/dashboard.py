from flask import Blueprint, render_template
from app.controllers.auth import login_required


dashboard = Blueprint('dashboard', __name__)


@dashboard.route("/dashboard", methods=['GET', 'POST'])
@login_required
def index():
    return render_template("dashboard/dashboard.html")




