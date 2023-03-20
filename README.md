# CubeServer

Status: `🟢 Complete`

Repository for Cube game data server. See documentation [here](https://hackmd.io/@samuelpswang/Hke6Z5zCj), and hosted app [here](http://ec2-35-177-122-51.eu-west-2.compute.amazonaws.com:5000/). Github Action is configured to auto-deploy on push to `main` branch.

| Key        | Value                                               |
| :--------- | :-------------------------------------------------- |
| Public DNS | `ec2-35-177-122-51.eu-west-2.compute.amazonaws.com` |
| Port       | `5000`                                              |

## API Documentation

### `/api`

* Method: `GET`, `POST`, `PUT`
* Request: `N/A`
* Response:

    ```html
    <pre>{Method} /api @ {Timestamp}</pre>
    ```

### `/api/user`

* Method: `GET`, `POST`, `PUT`
* Request:

    ```javascript
    {
        "username": str, // username of player
        "password": str // hashed password
    }
    ```

* Response:
  * `200 OK`: correct login

    ```javascript
    {
        "status": str, // "success"
        "message": str // success message
    }
    ```

  * `200 OK`: wrong login

    ```javascript
    {
        "status": str, // "failed"
        "message": str // fail message
    }
    ```

  * `400 Bad Request`

    ```javascript
    {
        "status": str, // "error"
        "type": str, // error type
        "message": str // error message
    }
    ```

### `/api/user/add`

* Method: `GET`, `POST`, `PUT`
* Request:

  ```javascript
  {
      "username": str, // username of player
      "password": str // hashed password
  }
  ```

* Response:
  * `200 OK`

    ```javascript
    {
        "status": str, // "success"
        "message": str // success message
    }
    ```

  * `400 Bad Request`

    ```javascript
    {
        "status": str, // "error"
        "type": str, // error type
        "message": str // error message
    }
    ```

### `/api/progress`

* Method: `GET`, `POST`, `PUT`
* Request:

  ```javascript
  {
      "username": str // username of player
  }
  ```

* Response:
  * `200 OK`

    ```javascript
    {
        "status": str, // "success"
        "data": {
            "score": [int], // score array
            "level": [int], // level array
            "progress": json, {
                    "timestamp": datetime, // timestamp of save
                    "data": json // game data that needs to be saved
            }
          }
    }
    ```

  * `400 Bad Request`

    ```javascript
    {
        "status": str, // "error"
        "type": str, // error type
        "message": str // error message
    }
    ```

### `/api/progress/update`

* Method: `GET`, `POST`, `PUT`
* Request:

  ```javascript
  {
      "username": str, // username of player requested
      "score": [int], // high score for each level
      "level": [int], // level status, (0: new, 1: in progress, 2: completed)
      "progress": json // game data that needs to be saved
  }
  ```

* Response:
  * `200 OK`
  
    ```javascript
    {
        "status": str, // "success",
        "message": str // success message
    }
    ```

  * `400 Bad Request`
  
    ```javascript
    {
        "status": str, // "error",
        "type": str, // error type,
        "message": str // error message
    }
    ```

### `/api/leaderboard`

* Method: `GET`, `POST`, `PUT`
* Request:

  ```javascript
  { 
      "count": int // number of players to return
  }
  ```

* Response:
  * `200 OK`

    ```javascript
    {
        "status": str, // "success"
        "data": {
            "level0": int, // level number
            "scores0": [str] // coresponding score of players from highscore to low
            "username0": [str], // username of players from highscore to low
            "level1": int, 
            "scores1": [str],
            "username1": [str],
            "level2": int,
            "scores2": [str]
            "username2": [str]
        }
    }
    ```

  * `400 Bad Request`
  
    ```javascript
    {
        "status": str, // "error"
        "type": str, // error type
        "message": str // error message
    }
    ```

## Development Quickstart

1. Clone this repository:

    ```bash
    git clone https://github.com/InformationProcessingProjectGroup4/CubeServer
    ```

2. Install latest version of Python; or check if you have `3.11.2` by `python --version`. If not, run the following:

    ```bash
    brew install python@3.11
    ```

3. Create the virtual environment and activate it:

    ```bash
    pip install virtualenv
    virtualenv --python=3.11.2 .venv
    source .venv/bin/activate
    ```

4. Go into the repo and install all dependancies:

    ```bash
    # You should now be in .../CubeServer
    pip install -r requirements.txt
    ```

5. Start the app:

    ```bash
    flask --app cubeserver run
    ```

6. To finish and exit the virtual environment:

    ```bash
    deactivate
    ```

## File Structure

```txt
CubeServer/
├─ .github/workflows
│  └─ github-actions-ec2.yml
├─ cubeserver/
│  ├─ __init__.py
│  ├─ views.py
│  ├─ db.py
│  └─ util.py
├─ tests/
│  └─ measure_rtt.py
├─ setup.py
├─ setup_db.py
├─ setup_db_clear.py
├─ deploy.sh
├─ cleanup.sh
└─ ...
```

1. Server Source Code
    1. `cubeserver/__init__.py`: main script for `cubeserver` package, initializes Flask app.
    2. `cubeserver/views.py`: routing script, handles different API endpoints.
    3. `cubeserver/db.py`: program script, handles communication with database.
    4. `cubeserver/util.py`: utility script, includes handy functions used in program & routing scripts.
2. Deployment Scripts
    1. `deploy.sh`: deployment script, kills current `tmux` session and start new session.
    2. `cleanup.sh`: utility script, removes python cache files.
    3. `.github/workflows/github-actions-ec2.yml`: utility script, describes steps to deployment for Github Actions.
3. Setup Scripts
    1. `setup.py`: setup script, lets `pip` knows what to install for deployment.
    2. `setup_db.py`: setup script, initializes DynamoDB table.
    3. `setup_db_clear.py`: setup script, removes the current DynamoDB table and create a empty new one.

## Branches

1. `main`: production branch.
2. `dev`: main developement branch, merge feature branches here (merged).
3. `feature/user`: development branch for `/user` endpoint (merged).
4. `feature/progress`: development branch for `/progress` endpoint (merged).
5. `feature/leaderboard`: development branch for `/leaderboard` endpoint (merged).
