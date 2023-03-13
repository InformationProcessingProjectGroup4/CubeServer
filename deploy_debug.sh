#!/bin/bash

# kill original session
tmux kill-session -t cubeserver

# create new session and run flask command
tmux new-session -d -s cubeserver "flask --app cubeserver --debug run --host 0.0.0.0 --port 5000"