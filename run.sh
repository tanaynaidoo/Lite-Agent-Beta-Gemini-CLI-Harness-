#!/bin/bash
# shellcheck disable=SC1091

# Simple script to manage the Lite Agent CLI for development/local testing.

VENV_PATH="./venv" # Updated to reflect 'venv' as per new README
PYTHON_EXEC="$VENV_PATH/bin/python"
CLI_COMMAND="esl-harness" # Use the installed CLI command

if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment '$VENV_PATH' not found. Please run 'python3 -m venv $VENV_PATH' and 'pip install -e .' (as per README)."
    exit 1
fi

if [ ! -f "$PYTHON_EXEC" ]; then
    echo "Python executable not found in virtual environment '$VENV_PATH'. Please ensure the virtual environment is correctly set up."
    exit 1
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Execute the CLI command directly, passing all arguments
exec "$CLI_COMMAND" "$@"
