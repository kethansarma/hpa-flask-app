#!/bin/bash
# start.sh

# Start Redis server in the background
redis-server --daemonize yes

# Wait a moment for Redis to start (optional, but good practice)
sleep 2

# Start Gunicorn (Flask app) in the foreground
# The `exec` command replaces the shell with the gunicorn process,
# ensuring signals (like SIGTERM from Kubernetes) are correctly handled.
# exec flask --app app run
exec gunicorn --bind 0.0.0.0:5000 app:app