#!/bin/bash
set -x
# This script builds the Windows executable for the Lite Agent CLI using PyInstaller.
# It also builds an NSIS installer for the generated executable.

# Exit immediately if a command exits with a non-zero status.
set -e

# Change to the script's directory first to ensure relative paths are correct
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Get architecture from argument, default to x64
ARCH="${1:-x64}" # Default to x64 if no argument provided

# Define paths
VENV_PATH="../../venv" # Relative path from script's directory (host/windows) to project root venv
BUILD_DIR="./build"
DIST_DIR="./dist"
MAIN_SCRIPT="../../main.py" # Relative path from script's directory (host/windows) to main.py
APP_NAME="esl-harness" # Desired name for the PyInstaller executable

# Start capturing build log
BUILD_LOG_FILE="build_debug_${ARCH}.log"
echo "--- Starting build_debug_${ARCH}.log ---" > "$BUILD_LOG_FILE"
echo "--- Building Windows Executable for Lite Agent CLI ($ARCH) ---" >> "$BUILD_LOG_FILE"

# 1. Check for virtual environment
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment '$VENV_PATH' not found. Please set up the development environment first (see main README)." >> "$BUILD_LOG_FILE"
    exit 1
fi

echo "Activating virtual environment..." >> "$BUILD_LOG_FILE"
# shellcheck disable=SC1091
source "$VENV_PATH/Scripts/activate" >> "$BUILD_LOG_FILE" 2>&1

VENV_PIP="$(cygpath -w "$VENV_PATH/Scripts/pip.exe")" # Use cygpath for Windows paths
VENV_PYINSTALLER="$(cygpath -w "$VENV_PATH/Scripts/pyinstaller.exe")" # Use cygpath for Windows paths


# 2. Install PyInstaller if not already installed
if ! command -v "$VENV_PYINSTALLER" &> /dev/null; then
    echo "PyInstaller not found in venv. Installing..." >> "$BUILD_LOG_FILE"
    "$VENV_PIP" install pyinstaller >> "$BUILD_LOG_FILE" 2>&1
else
    echo "PyInstaller already installed in venv." >> "$BUILD_LOG_FILE"
fi

# 3. Clean up previous build artifacts
echo "Cleaning up previous build artifacts..." >> "$BUILD_LOG_FILE"
# Remove potential previous installers (both x64 and x86)
rm -rf "$BUILD_DIR" "$DIST_DIR" "$APP_NAME.spec" "LiteAgentCLI_Installer_x64.exe" "LiteAgentCLI_Installer_x86.exe" >> "$BUILD_LOG_FILE" 2>&1

# 4. Run PyInstaller
WIN_MAIN_SCRIPT="$(cygpath -w "$MAIN_SCRIPT")"
WIN_DIST_DIR="$(cygpath -w "$DIST_DIR")"
WIN_BUILD_DIR="$(cygpath -w "$BUILD_DIR")"

echo "Running PyInstaller to create standalone executable ($ARCH)..." >> "$BUILD_LOG_FILE"
"$VENV_PYINSTALLER" \
    --noconfirm \
    --onefile \
    --console \
    --name "$APP_NAME" \
    --distpath "$WIN_DIST_DIR" \
    --workpath "$WIN_BUILD_DIR" \
    "$WIN_MAIN_SCRIPT" >> "$BUILD_LOG_FILE" 2>&1

echo "--- PyInstaller Build Complete ($ARCH) ---" >> "$BUILD_LOG_FILE"
echo "Standalone executable can be found in: $(pwd)/$DIST_DIR/$APP_NAME.exe" >> "$BUILD_LOG_FILE"

# 5. Build NSIS Installer
echo "--- Building NSIS Installer ($ARCH) ---" >> "$BUILD_LOG_FILE"

# Check if makensis is available
if ! command -v makensis &> /dev/null; then
    echo "makensis (NSIS compiler) not found. Please ensure NSIS is installed and in your PATH." >> "$BUILD_LOG_FILE"
    exit 1
fi

echo "Compiling NSIS script 'installer.nsi' for $ARCH..." >> "$BUILD_LOG_FILE"
makensis /V2 /L "makensis_internal_log.txt" /DARCH="$ARCH" installer.nsi >> "$BUILD_LOG_FILE" 2>&1

# Capture directory listing after makensis attempt
echo "--- Directory listing after makensis attempt ---" >> "$BUILD_LOG_FILE"
ls -l . >> "$BUILD_LOG_FILE" 2>&1
echo "--- End of directory listing ---" >> "$BUILD_LOG_FILE"

# Verify installer creation
INSTALLER_PATH="./LiteAgentCLI_Installer_${ARCH}.exe"
if [ ! -f "$INSTALLER_PATH" ]; then
    echo "ERROR: NSIS Installer '$INSTALLER_PATH' was not created!" >> "$BUILD_LOG_FILE"
    echo "--- Final directory listing ---" >> "$BUILD_LOG_FILE"
    ls -l . >> "$BUILD_LOG_FILE" 2>&1
    echo "--- End of final directory listing ---" >> "$BUILD_LOG_FILE"
    exit 1
fi
echo "NSIS Installer '$INSTALLER_PATH' successfully created." >> "$BUILD_LOG_FILE"

echo "--- All Windows Builds Complete ---" >> "$BUILD_LOG_FILE"
echo "--- End of build_debug_${ARCH}.log ---" >> "$BUILD_LOG_FILE"
