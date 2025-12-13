# src/lite_agent/cli.py
"""
Command-Line Interface (CLI) for the Lite Agent.

This module defines the CLI commands for interacting with the Lite Agent.
It acts as a thin wrapper that communicates with the running agent core
via IPC.
"""

import click

from .ipc import send_command_to_agent  # Import IPC function


@click.group()
def main():
    """Lite Agent CLI for managing the agent's operations."""
    # pylint: disable=unnecessary-pass # Pass is fine for Click groups


@main.command()
def start():
    """Starts the Lite Agent daemon."""
    click.echo("Attempting to start Lite Agent daemon...")
    response = send_command_to_agent({"command": "start_daemon"})
    click.echo(f"Lite Agent daemon start response: {response}")


@main.command()
def stop():
    """Stops the Lite Agent daemon."""
    click.echo("Attempting to stop Lite Agent daemon...")
    response = send_command_to_agent({"command": "stop_daemon"})
    click.echo(f"Lite Agent daemon stop response: {response}")


@main.command()
def status():
    """Checks the status of the Lite Agent daemon."""
    click.echo("Querying Lite Agent daemon status...")
    response = send_command_to_agent({"command": "status"})
    click.echo(f"Lite Agent status: {response}")


# Example of a subcommand group for configuration
@main.group()
def config():
    """Manage Lite Agent configuration."""
    # pylint: disable=unnecessary-pass # Pass is fine for Click groups


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
