from cubeserver import app

from flask import request
from datetime import datetime

# main api route; return method and timestamp
@app.route("/api", methods=["GET", "POST"])
def handle_root():
    return f"<pre>{request.method} /api @ {datetime.now()}</pre>"

# retrieve user data; return user data
@app.route("/api/user", methods=["GET", "POST"])
def handle_user():
    return f"<pre>{request.method} /api/user @ {datetime.now()}</pre>"

# save new user; returns user data
@app.route("/api/user/add", methods=["GET", "POST"])
def handle_user_add():
    return f"<pre>{request.method} /api/user/add @ {datetime.now()}</pre>"

# retrieve user progress; return progress data
@app.route("/api/progress", methods=["GET", "POST"])
def handle_progress():
    return f"<pre>{request.method} /api/progress @ {datetime.now()}</pre>"

# save user progress; returns new progress data
@app.route("/api/progress/update", methods=["GET", "POST"])
def handle_progress_update():
    return f"<pre>{request.method} /api/progress/update @ {datetime.now()}</pre>"

# retrieve leaderboard data; returns leaderboard data
@app.route("/api/leaderboard", methods=["GET", "POST"])
def handle_leaderboard():
    return f"<pre>{request.method} /api/leaderboard @ {datetime.now()}</pre>"
