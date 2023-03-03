from cubeserver import app, table
import cubeserver.db as db
from cubeserver.util import validate_score, validate_level
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
        return {"status": "error", "type": type(e).__name__, "message": str(e)}, 400
    else:
        if auth:
            return {"status": "success", "message": "password matched"}, 200
        else:
            return {"status": "failed", "message": "username or password incorrect"}, 200

# save new user; returns user data


@app.route("/api/user/add", methods=["POST"])
def handle_user_add():
    data = request.get_json(force=True)
    try:
        db.add_user(table, data["username"], data["password"])
    except Exception as e:
        return {"status": "error", "type": type(e).__name__, "message": str(e)}, 400
    else:
        return {"status": "success", "message": f"username ({data['username']}) added"}, 200

# retrieve user progress; return progress data


@app.route("/api/progress", methods=["POST"])
def handle_progress():
    data = request.get_json(force=True)
    if data['username']:
        try:
            score = db.get_user_score(table, data["username"])
            level = db.get_user_level(table, data["username"])
            progress = db.get_user_progress(table, data["username"])
        except Exception as e:
            return {"status": "error", "type": type(e).__name__, "message": str(e)}, 400
        else:
            return {"status": "success", "score": score, "level": level, "progress": progress}, 200
    else:
        return {"status": "error", "message": "username not provided"}, 400
        

# save user progress; returns new progress data


@app.route("/api/progress/update", methods=["POST"])
def handle_progress_update():
    data = request.get_json(force=True)
    if data['username']:
        if data["score"]:
            try:
                score = validate_score(data["score"])
                db.update_user_score(table, data["username"], score)
            except Exception as e:
                return {"status": "error", "type": type(e).__name__, "message": str(e)}, 400
        if data["level"]:
            try:
                level = validate_level(data["level"])
                db.update_user_level(table, data["username"], level)
            except Exception as e:
                return {"status": "error", "type": type(e).__name__, "message": str(e)}, 400
        if data["progress"]:
            try:
                db.update_user_progress(table, data["username"], data["progress"])
            except Exception as e:
                return {"status": "error", "type": type(e).__name__, "message": str(e)}, 400
        return {"status": "success", "message": f"updated with score ={score}, level={level}, progress={data['progress']}"}, 200
    else:
        return {"status": "error", "message": "username not provided"}, 400

# retrieve leaderboard data; returns leaderboard data


@app.route("/api/leaderboard", methods=["POST"])
def handle_leaderboard():
    return f"<pre>{request.method} /api/leaderboard @ {datetime.now()}</pre>"
