# Windows Support for Lite Agent CLI

This directory contains resources and instructions for building and using the Lite Agent CLI on Windows.

## Building the Executable

A standalone Windows executable (`.exe`) can be built using `PyInstaller`. This executable bundles the Python interpreter and all necessary dependencies, allowing the CLI to run on Windows systems without a Python installation.

### Prerequisites for Building

*   A Windows environment (either native Windows, WSL, or a CI/CD runner).
*   Python 3.10+ installed and available in your PATH.
*   `git` installed.
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
    This script will install `PyInstaller` (if not already present in your virtual environment), clean previous build artifacts, and then run `PyInstaller` to create the executable.

### Locating the Executable

After a successful build, the `esl-harness.exe` file will be located in the `host/windows/dist/` directory.

### Using the Executable

You can run the executable directly from your terminal:

```cmd
.\host\windows\dist\esl-harness.exe --help
```

or navigate to the `dist` folder and execute it.

## CI/CD Artifacts

The project's GitHub Actions workflow automatically builds the Windows executable on every push to `main` and `pull_request` to `main`. You can download the latest `esl-harness-windows-exe` artifact from the "Actions" tab of the GitHub repository after a successful build.

## Installation File (Future Work)

Currently, the built `.exe` is a standalone file. For a more traditional Windows installation experience (e.g., with an installer wizard, Start Menu shortcuts, uninstaller), further tools like NSIS or Inno Setup would be required. This is considered future work.
