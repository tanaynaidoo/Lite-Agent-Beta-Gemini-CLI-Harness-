#!/bin/bash

# Simple script to manage the Lite Agent CLI

VENV_PATH="./.venv"
PYTHON_EXEC="$VENV_PATH/bin/python"
CLI_ENTRYPOINT="src.lite_agent.cli"

if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found. Please run 'python3 -m venv .venv' and 'pip install -r requirements.txt'."
    exit 1
fi

if [ ! -f "$PYTHON_EXEC" ]; then
    echo "Python executable not found in virtual environment. Please run 'python3 -m venv .venv'."
    exit 1
fi

case "$1" in
    start)
        echo "Starting Lite Agent..."
        "$PYTHON_EXEC" -m "$CLI_ENTRYPOINT" start
        ;;
    stop)
        echo "Stopping Lite Agent..."
        "$PYTHON_EXEC" -m "$CLI_ENTRYPOINT" stop
        ;;
    status)
        echo "Checking Lite Agent status..."
        "$PYTHON_EXEC" -m "$CLI_ENTRYPOINT" status
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        exit 1
        ;;
esac