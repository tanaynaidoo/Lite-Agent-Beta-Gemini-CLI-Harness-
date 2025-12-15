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
# NSIS_INSTALLER_NAME will be defined by the NSIS script itself, but we can use it for reporting here

echo "--- Building Windows Executable for Lite Agent CLI ($ARCH) ---"

# 1. Check for virtual environment
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment '$VENV_PATH' not found. Please set up the development environment first (see main README)."
    exit 1
fi

echo "Activating virtual environment..."
# shellcheck disable=SC1091
source "$VENV_PATH/Scripts/activate"

VENV_PIP="$VENV_PATH/Scripts/pip.exe"
VENV_PYINSTALLER="$VENV_PATH/Scripts/pyinstaller.exe"


# 2. Install PyInstaller if not already installed
if ! command -v "$VENV_PYINSTALLER" &> /dev/null; then
    echo "PyInstaller not found in venv. Installing..."
    "$VENV_PIP" install pyinstaller
else
    echo "PyInstaller already installed in venv."
fi

# 3. Clean up previous build artifacts
echo "Cleaning up previous build artifacts..."
# Remove potential previous installers (both x64 and x86)
rm -rf "$BUILD_DIR" "$DIST_DIR" "$APP_NAME.spec" "LiteAgentCLI_Installer_x64.exe" "LiteAgentCLI_Installer_x86.exe"

# 4. Run PyInstaller
# Before PyInstaller call:
WIN_MAIN_SCRIPT="$(cygpath -w "$MAIN_SCRIPT")"
WIN_DIST_DIR="$(cygpath -w "$DIST_DIR")"
WIN_BUILD_DIR="$(cygpath -w "$BUILD_DIR")"

echo "Running PyInstaller to create standalone executable ($ARCH)..."
"$VENV_PYINSTALLER" \
    --noconfirm \
    --onefile \
    --console \
    --name "$APP_NAME" \
    --distpath "$WIN_DIST_DIR" \
    --workpath "$WIN_BUILD_DIR" \
    "$WIN_MAIN_SCRIPT"

echo "--- PyInstaller Build Complete ($ARCH) ---"
echo "Standalone executable can be found in: $(pwd)/$DIST_DIR/$APP_NAME.exe"

# 5. Build NSIS Installer
echo "--- Building NSIS Installer ($ARCH) ---"

# Check if makensis is available
if ! command -v makensis &> /dev/null; then
    echo "makensis (NSIS compiler) not found. Please ensure NSIS is installed and in your PATH."
    exit 1
fi

echo "Compiling NSIS script 'installer.nsi' for $ARCH..."
# Redirect makensis output and subsequent verification to a log file
BUILD_LOG="makensis_build_${ARCH}.log"
makensis /V2 /L "${BUILD_LOG}" /DARCH="$ARCH" installer.nsi > "${BUILD_LOG}" 2>&1
echo "--- Contents of ${BUILD_LOG} ---"
cat "${BUILD_LOG}"
echo "--- End of ${BUILD_LOG} ---"

# Verify installer creation
INSTALLER_PATH="./LiteAgentCLI_Installer_${ARCH}.exe"
if [ ! -f "$INSTALLER_PATH" ]; then
    echo "ERROR: NSIS Installer '$INSTALLER_PATH' was not created!"
    echo "--- Listing current directory (host/windows/) contents ---"
    ls -l .
    echo "--- End of directory listing ---"
    exit 1
fi
echo "NSIS Installer '$INSTALLER_PATH' successfully created."

echo "--- NSIS Installer Build Complete ($ARCH) ---"
echo "Installer can be found in: $(pwd)/LiteAgentCLI_Installer_${ARCH}.exe" # Dynamic name based on ARCH

echo "--- All Windows Builds Complete ---"
