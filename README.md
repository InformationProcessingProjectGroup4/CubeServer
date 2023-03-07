# CubeServer

Repository for Cube game data server. See documentation [here](https://hackmd.io/@samuelpswang/Hke6Z5zCj).

## Quickstart

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
    pip install -e .
    ```

5. Make an empty `config.py`, will add needed configurations later:

    ```sh
    touch config.py
    ```

6. Start the app:

    ```sh
    flask --app cubeserver run
    ```

7. To finish and exit the virtual environment:

    ```sh
    deactivate
    ```

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

    ```json
    {
        "username": str, username of player,
        "password": str, hashed password
    }
    ```

* Response:
  * `200 OK`: correct login

    ```json
    {
        "status": str, "success",
        "message": str, success message
    }
    ```

  * `200 OK`: wrong login

    ```json
    {
        "status": str, "failed",
        "message": str, fail message
    }
    ```

  * `400 Bad Request`

    ```json
    {
        "status": str, "error",
        "type": str, error type,
        "message": str, error message
    }
    ```

### `/api/user/add`

* Method: `POST`
* Request:

  ```json
  {
      "username": str, username of player,
      "password": str, hashed password
  }
  ```

* Response:
  * `200 OK`

    ```json
    {
        "status": str, "success",
        "message": str, success message
    }
    ```

  * `400 Bad Request`

    ```json
    {
        "status": str, "error",
        "type": str, error type,
        "message": str, error message
    }
    ```

### `/api/progress`

* Method: `POST`
* Request:

  ```json
  {
      "username": str, username of player
  }
  ```

* Response:
  * `200 OK`

    ```json
    {
        "status": str, "success",
        "data": {
            "score": [str], score array
            "level": [str], level array
            "progress": json, {
                    "timestamp": datetime, timestamp of save,
                    "data": json, game data that needs to be saved
            }
          }
    }
    ```

  * `400 Bad Request`

    ```json
    {
        "status": str, "error",
        "type": str, error type,
        "message": str, error message
    }
    ```

### `/api/progress/update`

* Method: `POST`
* Request:

  ```json
  {
      "username": str, username of player requested,
      "score": [int], [int], high score for each level
      "level": [int], level status, (0: new, 1: in progress, 2: completed)
      "progress": json, game data that needs to be saved
  }
  ```

* Response:
  * `200 OK`
  
    ```json
    {
        "status": str, "success",
        "message": str, success message
    }
    ```

  * `400 Bad Request`
  
    ```json
    {
        "status": str, "error",
        "type": str, error type,
        "message": str, error message
    }
    ```

### `/api/leaderboard`

* Method: `POST`
* Request:

  ```json
  [{ 
      "level": int, level number,
      "count": int, number of players to return
  }]
  ```

* Response:
  * `200 OK`

    ```json
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
  
    ```json
    {
        "status": str, "error",
        "type": str, error type,
        "message": str, error message
    }
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
2. `dev`: main developement branch, merge feature branches here.
3. `feature/user`: development branch for `/user` endpoint.
4. `feature/progress`: development branch for `/progress` endpoint.
5. `feature/leaderboard`: development branch for `/leaderboard` endpoint.
