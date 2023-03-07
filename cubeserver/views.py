from cubeserver import app, table
import cubeserver.db as db

from flask import request
from datetime import datetime

# main api route; return method and timestamp
@app.route("/api", methods=["GET", "POST"])
def handle_root():
    return f"<pre>{request.method} /api @ {datetime.now()}</pre>"

# retrieve user data; return user data
@app.route("/api/user", methods=["POST"])
def handle_user():
    data = request.get_json(force=True)
    try:
        auth = db.auth_user(table, data["username"], data["password"])
    except Exception as e:
        return { "status": "error", "type": type(e).__name__, "message": str(e)}, 400
    else:
        if auth:
            return { "status": "success", "message": "password matched" }, 200
        else:
            return { "status": "failed", "message": "username or password incorrect" }, 200

# save new user; returns user data
@app.route("/api/user/add", methods=["POST"])
def handle_user_add():
    data = request.get_json(force=True)
    try:
        success = db.add_user(table, data["username"], data["password"])
    except Exception as e:
        return { "status": "error", "type": type(e).__name__, "message": str(e)}, 400
    else:
        if success:
            return { "status": "success", "message": f"username ({data['username']}) added" }, 200
        else:
            return { "status": "failed", "message": f"username ({data['username']}) already in database" }, 200

# retrieve user progress; return progress data
@app.route("/api/progress", methods=["POST"])
def handle_progress():
    return f"<pre>{request.method} /api/progress @ {datetime.now()}</pre>"

# save user progress; returns new progress data
@app.route("/api/progress/update", methods=["POST"])
def handle_progress_update():
    return f"<pre>{request.method} /api/progress/update @ {datetime.now()}</pre>"

# retrieve leaderboard data; returns leaderboard data
@app.route("/api/leaderboard", methods=["POST"])
def handle_leaderboard():
    return f"<pre>{request.method} /api/leaderboard @ {datetime.now()}</pre>"
