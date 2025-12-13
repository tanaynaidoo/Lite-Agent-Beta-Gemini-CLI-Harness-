# src/lite_agent/cli.py
"""
Command-Line Interface (CLI) for the Lite Agent.

This module defines the CLI commands for interacting with the Lite Agent.
It acts as a thin wrapper that communicates with the running agent core
via IPC.
"""

import os
import signal  # Added for signal.SIGKILL
import subprocess
import sys
import time

import click

# Import IPC functions and PID_FILE
# flake8: noqa: F401 (UDS_PATH is not directly used, but PID_FILE is)
# pylint: disable=W0611 # UDS_PATH is not directly used in this file
from .ipc import PID_FILE, UDS_PATH, send_command_to_agent


@click.group()
def main():
    """Lite Agent CLI for managing the agent's operations."""
    # pylint: disable=unnecessary-pass # Pass is fine for Click groups
    pass


@main.command()
def start():
    """Starts the Lite Agent daemon."""
    click.echo("Attempting to start Lite Agent daemon...")

    if os.path.exists(PID_FILE):
        click.echo(f"PID file found at {PID_FILE}. Agent might already be running.")
        try:
            with open(PID_FILE, "r", encoding="utf-8") as f:  # pylint: disable=W1514
                pid = int(f.read().strip())
            # Check if process exists
            if pid > 0 and os.path.exists(f"/proc/{pid}"):  # pylint: disable=C0301
                click.echo(f"Agent is already running with PID: {pid}. Exiting.")
                sys.exit(1)
            else:
                click.echo("Stale PID file found. Removing...")
                os.remove(PID_FILE)
        except (ValueError, FileNotFoundError):
            pass  # Invalid PID file or not found, proceed

    # Run agent_core.py as a detached subprocess
    # This will execute the _daemonize function inside agent_core.py
    # We use python executable from the virtual environment
    python_executable = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".venv",
        "bin",
        "python",
    )
    if not os.path.exists(python_executable):
        click.echo("Error: Python executable not found in ./.venv/bin.")
        click.echo("Please ensure virtual environment is set up and activated once.")
        sys.exit(1)

    try:
        # Popen is non-blocking. The daemon will fork and exit this parent.
        # stdout/stderr are redirected in _daemonize()
        subprocess.Popen(
            [python_executable, "-m", "src.lite_agent.agent_core"],
            start_new_session=True,  # Decouple from controlling process group
        )
        click.echo("Lite Agent daemon initiated. Check logs for status.")

        # Give a moment for the daemon to start and write PID
        time.sleep(1)
        if os.path.exists(PID_FILE):
            with open(PID_FILE, "r", encoding="utf-8") as f:  # pylint: disable=W1514
                pid = int(f.read().strip())
            click.echo(f"Agent should be running with PID: {pid}")
        else:
            click.echo("Could not find PID file. Daemon might have failed to start.")

    except (FileNotFoundError, PermissionError, OSError) as err:
        click.echo(f"Error starting daemon: {err}", err=True)
        sys.exit(1)


@main.command()
def stop():
    """Stops the Lite Agent daemon."""
    click.echo("Attempting to stop Lite Agent daemon...")
    response = send_command_to_agent({"command": "stop_daemon"})
    click.echo(f"Lite Agent daemon stop response: {response}")

    # Also check if PID file exists after sending stop command and clean up
    if os.path.exists(PID_FILE):
        try:
            # pylint: disable=W1514,R1732
            with open(PID_FILE, "r", encoding="utf-8") as f:
                pid = int(f.read().strip())
            # Give agent some time to shut down gracefully
            time.sleep(1)
            # Check if process exists before attempting to kill
            if os.path.exists(f"/proc/{pid}"):
                click.echo(f"Agent with PID {pid} is still running after stop command.")
                click.echo("Attempting to send SIGKILL to ensure termination.")
                os.kill(pid, signal.SIGKILL)
                click.echo(f"SIGKILL sent to PID {pid}.")
            else:
                click.echo(f"Agent with PID {pid} is no longer running.")

            os.remove(PID_FILE)
            click.echo("PID file removed.")
        except (ValueError, FileNotFoundError, OSError) as err:
            click.echo(f"Error during post-stop cleanup: {err}", err=True)
    elif response.get("error") != "Agent not running or socket missing.":
        click.echo("No PID file found. Agent might have already been stopped.")


@main.command()
def status():
    """Checks the status of the Lite Agent daemon."""
    click.echo("Querying Lite Agent daemon status...")
    if not os.path.exists(PID_FILE):
        click.echo("Agent is not running (PID file not found).")
        return

    try:
        # pylint: disable=W1514,R1732
        with open(PID_FILE, "r", encoding="utf-8") as f:
            pid = int(f.read().strip())
        if pid > 0 and os.path.exists(f"/proc/{pid}"):
            click.echo(f"Agent is running with PID: {pid}")
            response = send_command_to_agent({"command": "status"})
            if "status" in response:
                click.echo(f"Agent internal status: {response['status']}")
            else:
                click.echo(
                    f"Agent internal query error: {response.get('error', 'Unknown')}"
                )
        else:
            click.echo(
                f"Agent is not running (stale PID {pid} found). "
                f"Removing PID file {PID_FILE}."
            )
            os.remove(PID_FILE)
    except (ValueError, FileNotFoundError, OSError) as err:  # pylint: disable=W0718
        click.echo(
            f"Error checking agent status: {err}. "
            f"Removing PID file {PID_FILE} if present."
        )
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)


# Example of a subcommand group for configuration
@main.group()
def config():
    """Manage Lite Agent configuration."""
    # pylint: disable=unnecessary-pass # Pass is fine for Click groups
    pass


@config.command(name="get")
@click.argument("key")
def get_config(key):
    """Retrieves a configuration value."""
    click.echo(f"Getting config for key: {key} (placeholder)")


@config.command(name="set")
@click.argument("key")
@click.argument("value")
def set_config(key, value):
    """Sets a configuration value."""
    click.echo(f"Setting config '{key}' to '{value}' (placeholder)")


@config.command(name="show")
def show_config():
    """Shows the current configuration."""
    click.echo("Showing current configuration (placeholder).")


if __name__ == "__main__":
    main()
