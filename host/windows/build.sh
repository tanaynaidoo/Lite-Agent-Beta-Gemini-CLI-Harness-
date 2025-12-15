#!/bin/bash
set -x
# This script builds the Windows executable for the Lite Agent CLI using PyInstaller.
# It also builds an NSIS installer for the generated executable.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "build.sh started"

# Get architecture from argument, default to x64
ARCH="${1:-x64}" # Default to x64 if no argument provided
echo "Architecture: $ARCH"

echo "build.sh finished"
