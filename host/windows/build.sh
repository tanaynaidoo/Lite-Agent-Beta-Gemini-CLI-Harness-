#!/bin/bash
# This script builds the Windows executable for the Lite Agent CLI using PyInstaller.

# Exit immediately if a command exits with a non-zero status.
set -e

# Define paths
VENV_PATH="../../venv" # Relative path to the virtual environment
BUILD_DIR="./build"
DIST_DIR="./dist"
MAIN_SCRIPT="../../main.py" # Relative path to the main entry point
APP_NAME="esl-harness" # Desired name for the executable

echo "--- Building Windows Executable for Lite Agent CLI ---"

# 1. Check for virtual environment and activate it
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment '$VENV_PATH' not found. Please set up the development environment first (see main README)."
    exit 1
fi

echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# 2. Install PyInstaller if not already installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
else
    echo "PyInstaller already installed."
fi

# 3. Clean up previous build artifacts
echo "Cleaning up previous build artifacts..."
rm -rf "$BUILD_DIR" "$DIST_DIR" "$APP_NAME.spec"

# 4. Run PyInstaller
echo "Running PyInstaller..."
# Using --noconfirm to avoid interactive prompts
pyinstaller \
    --noconfirm \
    --onefile \
    --console \
    --name "$APP_NAME" \
    --distpath "$DIST_DIR" \
    --workpath "$BUILD_DIR" \
    "$MAIN_SCRIPT"

echo "--- Build Complete ---"
echo "Executable can be found in: $(pwd)/$DIST_DIR/$APP_NAME.exe"
