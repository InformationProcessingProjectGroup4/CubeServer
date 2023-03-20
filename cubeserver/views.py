from flask import request
from datetime import datetime

from cubeserver import app, table
import cubeserver.db as db
from cubeserver.util import validate_score, validate_level


# main api route; return method and timestamp
@app.route("/", methods=["GET", "POST", "PUT"])
def handle_root():
    return f"<h1>Welcome to <code>CubeServer-Test-3</code></h1><p>by T. Chung, A. Kohli, R. Shek, B. Sukumaran, G. Vasandani, S. Wang</p>>"

@app.route("/api", methods=["GET", "POST", "PUT"])
def handle_api():
    return f"<pre>{request.method} /api @ {datetime.now()}</pre>"


# retrieve user data; return user data
@app.route("/api/user", methods=["GET", "POST", "PUT"])
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
@app.route("/api/user/add", methods=["GET", "POST", "PUT"])
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
@app.route("/api/progress", methods=["GET", "POST", "PUT"])
def handle_progress():
    data = request.get_json(force=True)
    if 'username' in data:
        try:
            serverResponse = db.get_user_data(table, data["username"])
            score = serverResponse["score"]
            for i in range(len(score)):
                score[i] = int(score[i])
            level = serverResponse["level"]
            for i in range(len(level)):
                level[i] = int(level[i])
            progress = serverResponse["progress"]
        except Exception as e:
            return {"status": "error", "type": type(e).__name__, "message": str(e)}, 400
        else:
            return {"status": "success", "score": score, "level": level, "progress": progress }, 200
    else:
        return {"status": "error", "message": "username not provided"}, 400

# save user progress; returns new progress data
@app.route("/api/progress/update", methods=["GET", "POST", "PUT"])
def handle_progress_update():
    data = request.get_json(force=True)
    message ="Updated with "
    if 'username' in data:
        if 'score' in data:
            try:
                score = validate_score(data["score"])
                db.update_user_score(table, data["username"], score)
                message += f"score={score}, "
            except Exception as e:
                return {"status": "error", "type": type(e).__name__, "message": str(e)}, 400
        if 'level' in data:
            try:
                level = validate_level(data["level"])
                db.update_user_level(table, data["username"], level)
                message += f"level={level}, "
            except Exception as e:
                return {"status": "error", "type": type(e).__name__, "message": str(e)}, 400
        if 'progress' in data:
            try:
                db.update_user_progress(table, data["username"], data["progress"])
                message += f"progress={data['progress']}, "
            except Exception as e:
                return {"status": "error", "type": type(e).__name__, "message": str(e)}, 400
        return {"status": "success", "message": message}, 200
    else:
        return {"status": "error", "message": "username not provided"}, 400


# retrieve leaderboard data; returns leaderboard data
@app.route("/api/leaderboard", methods=["GET", "POST", "PUT"])
def handle_leaderboard():
    req_data = request.get_json(force=True) #array of dictionaries
    try:
        res_data = []
        for data in req_data:
            leaderboard = db.get_leaderboard(table, data["level"], data["count"])
            res_data.append(leaderboard)
    except Exception as e:
        return { "status": "error", "type": type(e).__name__, "message": str(e) }, 400
    else:
        return { "status": "success", "data": res_data }, 200
