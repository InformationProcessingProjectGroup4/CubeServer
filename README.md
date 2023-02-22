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
    cd cubeserver
    pip install -r requirements.txt
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
