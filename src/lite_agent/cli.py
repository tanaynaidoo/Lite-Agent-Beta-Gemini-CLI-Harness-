# src/lite_agent/cli.py
"""
Command-Line Interface (CLI) for the Lite Agent.
The human interface to our AI companion.

This module defines the CLI commands for interacting with the Lite Agent.
It acts as a thin wrapper that communicates with the running agent core
via IPC, translating human intent into digital directives.
"""

import json
import os
import signal  # Added for signal.SIGKILL
import subprocess
import sys
import time

import click
import psutil

from .ipc import PID_FILE, send_command_to_agent

CONFIG_DIR = click.get_app_dir("lite-agent")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


@click.group()
def main():
    """Lite Agent CLI for managing the agent's operations.
    The console where human and AI collaborate.
    """
    # pylint: disable=unnecessary-pass # Pass is fine for Click groups
    pass


@main.command()
def start():
    """Starts the Lite Agent daemon.
    Awaken the AI, initiate its autonomous journey.
    """
    click.echo("Attempting to start Lite Agent daemon... The AI is booting up.")

    if os.path.exists(PID_FILE):
        click.echo(f"PID file found at {PID_FILE}. Agent might already be running.")
        try:
            with open(PID_FILE, "r", encoding="utf-8") as f:
                pid = int(f.read().strip())
            # Check if process exists in the system's process table
            if pid > 0 and psutil.pid_exists(pid):
                click.echo(
                    f"Agent is already running with PID: {pid}. "
                    "A watchful AI is already at its post. Exiting."
                )
                sys.exit(1)
            else:
                click.echo(
                    "Stale PID file found. Removing... "
                    "Clearing the path for a fresh start."
                )
                os.remove(PID_FILE)
        except (ValueError, FileNotFoundError):
            # Invalid PID file or not found, proceed to start
            pass

    # Launch agent_core.py as a detached subprocess.
    # This command is the human's call to bring the agent to life.
    python_executable = sys.executable
    if not os.path.exists(python_executable):
        click.echo(
            "Error: Python executable not found. "
            "This is unexpected, please check your environment.",
            err=True,
        )
        sys.exit(1)

    try:
        # Popen is non-blocking. The daemon will fork and detach.
        subprocess.Popen(
            [python_executable, "-m", "src.lite_agent.agent_core"],
            start_new_session=True,  # Decouple from controlling process group
        )
        click.echo(
            "Lite Agent daemon initiated. Check logs for the AI's first thoughts."
        )

        # Wait for the daemon to start and write its PID file
        start_time = time.time()
        while not os.path.exists(PID_FILE):
            if time.time() - start_time > 5:
                click.echo(
                    "Could not find PID file after 5 seconds. Daemon might have failed to start. "
                    "Consult the logs for diagnostics.",
                    err=True,
                )
                sys.exit(1)
            time.sleep(0.1)

        with open(PID_FILE, "r", encoding="utf-8") as f:
            pid = int(f.read().strip())
        click.echo(f"Agent is now operational with PID: {pid}. Your AI is ready.")

    except (FileNotFoundError, PermissionError, OSError) as err:
        click.echo(
            f"Error starting daemon: {err}. "
            "Failed to launch the AI's core. Review permissions or path.",
            err=True,
        )
        sys.exit(1)


@main.command()
def stop():
    """Stops the Lite Agent daemon.
    Command the AI to stand down, ensuring a graceful conclusion to its tasks.
    """
    click.echo("Attempting to stop Lite Agent daemon... Initiating shutdown sequence.")
    response = send_command_to_agent({"command": "stop_daemon"})
    click.echo(f"Lite Agent daemon stop response: {response}")

    # After sending the stop command, verify termination and clean up.
    if os.path.exists(PID_FILE):
        try:
            # pylint: disable=W1514,R1732
            with open(PID_FILE, "r", encoding="utf-8") as f:
                pid = int(f.read().strip())

            # Give agent some time to shut down gracefully
            time.sleep(2)
            if psutil.pid_exists(pid):
                click.echo(f"Agent with PID {pid} is still running. Sending SIGTERM.")
                os.kill(pid, signal.SIGTERM)
                time.sleep(3)
                if psutil.pid_exists(pid):
                    click.echo(
                        f"Agent with PID {pid} did not respond to SIGTERM. Sending SIGKILL."
                    )
                    os.kill(pid, signal.SIGKILL)
                    click.echo(f"SIGKILL sent to PID {pid}.")

            if not psutil.pid_exists(pid):
                click.echo(
                    f"Agent with PID {pid} is no longer running. The AI has gracefully retired."
                )

            os.remove(PID_FILE)
            click.echo("PID file removed. A clean slate for the next activation.")
        except (ValueError, FileNotFoundError, OSError) as err:
            click.echo(
                f"Error during post-stop cleanup: {err}. "
                "Manual PID file removal may be required.",
                err=True,
            )
    elif response.get("error") != "Agent not running or socket missing.":
        click.echo(
            "No PID file found. Agent might have already been stopped. "
            "The AI was already resting."
        )


@main.command()
def status():
    """Checks the status of the Lite Agent daemon.
    Inquire about the AI's current operational state.
    """
    click.echo("Querying Lite Agent daemon status... Reaching out to the AI's core.")
    if not os.path.exists(PID_FILE):
        click.echo(
            "Agent is not running (PID file not found). "
            "The AI's presence is not detected in the system.",
            err=True,
        )
        return

    try:
        # pylint: disable=W1514,R1732
        with open(PID_FILE, "r", encoding="utf-8") as f:
            pid = int(f.read().strip())
        if pid > 0 and psutil.pid_exists(pid):
            click.echo(
                f"Agent is running with PID: {pid}. The AI is actively processing."
            )
            response = send_command_to_agent({"command": "status"})
            if "status" in response:
                click.echo(f"Agent internal status: {response['status']}")
            else:
                click.echo(
                    f"Agent internal query error: {response.get('error', 'Unknown')}. "
                    "The AI's internal monologue is interrupted."
                )
        else:
            click.echo(
                f"Agent is not running (stale PID {pid} found). "
                f"Removing PID file {PID_FILE}. The AI's previous footprint is cleared."
            )
            os.remove(PID_FILE)
    except (ValueError, FileNotFoundError, OSError) as err:  # pylint: disable=W0718
        click.echo(
            f"Error checking agent status: {err}. "
            f"Removing PID file {PID_FILE} if present. The AI's status is ambiguous.",
            err=True,
        )
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)


def load_config():
    """Loads the configuration from the JSON file."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_config(config_data):
    """Saves the configuration to the JSON file."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)


# Example of a subcommand group for configuration
@main.group()
def config():
    """Manage Lite Agent configuration.
    Adjust the AI's parameters, fine-tuning its behavior.
    """
    pass


@config.command(name="get")
@click.argument("key")
def get_config(key):
    """Retrieves a configuration value.
    Inquire about a specific parameter guiding the AI.
    """
    config_data = load_config()
    value = config_data.get(key)
    if value is not None:
        click.echo(f"{key}: {value}")
    else:
        click.echo(f"Configuration key '{key}' not found.", err=True)


@config.command(name="set")
@click.argument("key")
@click.argument("value")
def set_config(key, value):
    """Sets a configuration value.
    Impart new directives to shape the AI's operational parameters.
    """
    config_data = load_config()
    config_data[key] = value
    save_config(config_data)
    click.echo(f"Set '{key}' to '{value}'. The AI absorbs new instructions.")


@config.command(name="show")
def show_config():
    """Shows the current configuration.
    Display the full blueprint of the AI's current operational state.
    """
    config_data = load_config()
    if config_data:
        click.echo(json.dumps(config_data, indent=4))
    else:
        click.echo("No configuration set. The AI's mind is a blank slate.")


if __name__ == "__main__":
    main()
