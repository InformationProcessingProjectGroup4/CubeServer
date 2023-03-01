from flask import Flask
import os

from cubeserver.db import db_connect

# create app
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# create instance folder
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# connect database
table = db_connect("CubeServerData")

# import views
import cubeserver.views


if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"])