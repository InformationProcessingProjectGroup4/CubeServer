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
