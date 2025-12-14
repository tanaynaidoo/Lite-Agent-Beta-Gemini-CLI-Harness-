# Windows Support for Lite Agent CLI

This directory contains resources and instructions for building and using the Lite Agent CLI on Windows.

## Building the Executable and Installer

The Lite Agent CLI for Windows is distributed as a user-friendly installer (`.exe`) that bundles the PyInstaller-generated standalone executable. This installer is created using NSIS (Nullsoft Scriptable Install System).

### Prerequisites for Building

*   A Windows environment (either native Windows, WSL, or a CI/CD runner).
*   Python 3.10+ installed and available in your PATH.
*   `git` installed.
*   **NSIS (Nullsoft Scriptable Install System)** installed and `makensis` available in your PATH.
*   Your local development environment set up as described in the main project `README.md` (including virtual environment and `pip install -e .`).

### Steps to Build

1.  **Open a Terminal:** Navigate to the project root in a terminal (e.g., Git Bash, PowerShell, Command Prompt).
2.  **Ensure Virtual Environment is Active:** If you're building locally, activate your project's virtual environment.
    ```bash
    source venv/bin/activate
    ```
    *(Note: This step might differ slightly in PowerShell or Command Prompt. In PowerShell, you might use `./venv/Scripts/Activate.ps1`)*
3.  **Run the Build Script:** Execute the provided `build.sh` script located in this directory.
    ```bash
    ./host/windows/build.sh
    ```
    This script will:
    *   Install `PyInstaller` (if not already present).
    *   Build the standalone `esl-harness.exe` using `PyInstaller`.
    *   Compile the NSIS script (`installer.nsi`) to create the final installer.

### Locating the Installer

After a successful build, the NSIS installer `LiteAgentCLI_Installer_x64.exe` will be located in the `host/windows/` directory.

### Using the Installer

Simply run the `LiteAgentCLI_Installer_x64.exe` file on your Windows machine and follow the on-screen instructions. This will install the Lite Agent CLI, create Start Menu shortcuts, and register it for uninstallation.

## CI/CD Artifacts

The project's GitHub Actions workflow automatically builds the Windows installer on every push to `main` and `pull_request` to `main`. You can download the latest `LiteAgentCLI_Installer_x64.exe` artifact from the "Actions" tab of the GitHub repository after a successful build.
```