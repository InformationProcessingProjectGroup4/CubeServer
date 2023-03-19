# CubeServer

Status: `🟢 Complete`

Repository for Cube game data server. See documentation [here](https://hackmd.io/@samuelpswang/Hke6Z5zCj), and hosted app [here](http://ec2-35-177-122-51.eu-west-2.compute.amazonaws.com:5000/). Github Action is configured to auto-deploy on push to `main` branch.

| Key        | Value                                               |
| :--------- | :-------------------------------------------------- |
| Public DNS | `ec2-35-177-122-51.eu-west-2.compute.amazonaws.com` |
| Port       | `5000`                                              |

## API Documentation

### `/api`

* Method: `GET, POST`
* Request: `N/A`
* Response:

    ```txt
    <pre>{Method} /api @ {Timestamp}</pre>
    ```

### `/api/user`

* Method: `POST`
* Request:

    ```
    {
        "username": str, username of player,
        "password": str, hashed password
    }
    ```

* Response:
  * `200 OK`: correct login

    ```
    {
        "status": str, "success",
        "message": str, success message
    }
    ```

  * `200 OK`: wrong login

    ```
    {
        "status": str, "failed",
        "message": str, fail message
    }
    ```

  * `400 Bad Request`

    ```
    {
        "status": str, "error",
        "type": str, error type,
        "message": str, error message
    }
    ```

### `/api/user/add`

* Method: `POST`
* Request:

  ```
  {
      "username": str, username of player,
      "password": str, hashed password
  }
  ```

* Response:
  * `200 OK`

    ```
    {
        "status": str, "success",
        "message": str, success message
    }
    ```

  * `400 Bad Request`

    ```
    {
        "status": str, "error",
        "type": str, error type,
        "message": str, error message
    }
    ```

### `/api/progress`

* Method: `POST`
* Request:

  ```
  {
      "username": str, username of player
  }
  ```

* Response:
  * `200 OK`

    ```
    {
        "status": str, "success",
        "data": {
            "score": [int], score array
            "level": [int], level array
            "progress": json, {
                    "timestamp": datetime, timestamp of save,
                    "data": json, game data that needs to be saved
            }
          }
    }
    ```

  * `400 Bad Request`

    ```
    {
        "status": str, "error",
        "type": str, error type,
        "message": str, error message
    }
    ```

### `/api/progress/update`

* Method: `POST`
* Request:

  ```
  {
      "username": str, username of player requested,
      "score": [int], [int], high score for each level
      "level": [int], level status, (0: new, 1: in progress, 2: completed)
      "progress": json, game data that needs to be saved
  }
  ```

* Response:
  * `200 OK`
  
    ```
    {
        "status": str, "success",
        "message": str, success message
    }
    ```

  * `400 Bad Request`
  
    ```
    {
        "status": str, "error",
        "type": str, error type,
        "message": str, error message
    }
    ```

### `/api/leaderboard`

* Method: `POST`
* Request:

  ```
  [{ 
      "level": int, level number,
      "count": int, number of players to return
  }]
  ```

* Response:
  * `200 OK`

    ```
    {
        "status": str, "success",
        "data": [{
            "level": int, level number,
            "players": [str], username of players from highscore to low,
            "scores": [int], coresponding score of players from highscore to low
        }]
    }
    ```

  * `400 Bad Request`
  
    ```
    {
        "status": str, "error",
        "type": str, error type,
        "message": str, error message
    }
    ```

## Development Quickstart

1. Clone this repository:

    ```sh
    git clone https://github.com/InformationProcessingProjectGroup4/CubeServer
    ```

2. Install latest version of Python; or check if you have `3.11.2` by `python --version`. If not, run the following:

    ```sh
    brew install python@3.11
    ```

3. Create the virtual environment and activate it:

    ```sh
    pip install virtualenv
    virtualenv --python=3.11.2 .venv
    source .venv/bin/activate
    ```

4. Go into the repo and install all dependancies:

    ```sh
    # You should now be in .../CubeServer
    pip install -r requirements.txt
    ```

5. Start the app:

    ```sh
    flask --app cubeserver run
    ```

6. To finish and exit the virtual environment:

    ```sh
    deactivate
    ```

## File Structure

```txt
CubeServer/
├─ cubeserver/
│  ├─ __init__.py
│  ├─ views.py
│  └─ db.py
├─ test/
├─ setup.py
├─ config.py
├─ requirements.txt
├─ .gitignore
└─ README.md
```

1. `cubeserver/__init__.py`: main script for `cubeserver` package, initializes Flask app.
2. `cubeserver/views.py`: routing script, handles different API endpoints.
3. `cubeserver/db.py`: program script, handles communication with database.
4. `setup.py`: setup script, lets `pip` knows what to install.

## Branches

1. `main`: production branch.
2. `dev`: main developement branch, merge feature branches here (merged).
3. `feature/user`: development branch for `/user` endpoint (merged).
4. `feature/progress`: development branch for `/progress` endpoint (merged).
5. `feature/leaderboard`: development branch for `/leaderboard` endpoint (merged).
