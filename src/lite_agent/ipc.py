# src/lite_agent/ipc.py
"""
Inter-Process Communication (IPC) mechanisms for the Lite Agent.

This module handles communication between the CLI and the running agent daemon.
It will primarily use Unix Domain Sockets for efficient and secure local communication.
"""

import json
import logging
import os
import socket

# flake8: noqa: E501 (Ignoring line length for UDS_PATH definition if it gets long)

# Define the Unix Domain Socket path
# This should ideally be configurable and located in a secure, writable path
# For example, in /var/run/lite_agent.sock for system services,
# or a user-specific path in ~/.cache/lite_agent/lite_agent.sock
UDS_PATH = "/tmp/lite_agent.sock"


def send_command_to_agent(command_dict):
    """
    Sends a command to the running Lite Agent daemon via Unix Domain Socket.
    """
    if not os.path.exists(UDS_PATH):
        logging.error("Agent socket not found at %s. Is the agent running?", UDS_PATH)
        return {"error": "Agent not running or socket missing."}

    try:
        client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client_socket.connect(UDS_PATH)

        message = json.dumps(command_dict)
        client_socket.sendall(message.encode("utf-8"))

        # Receive response
        response_data = client_socket.recv(4096).decode("utf-8")
        response_dict = json.loads(response_data)

        client_socket.close()
        return response_dict
    except FileNotFoundError:
        logging.error("Unix Domain Socket file not found: %s", UDS_PATH)
        return {"error": "Socket file not found."}
    except ConnectionRefusedError:
        logging.error(
            "Connection refused. Agent might be restarting or " "unresponsive."
        )
        return {"error": "Agent refused connection."}
    except Exception as err:  # pylint: disable=broad-exception-caught
        # Catching broad exception for now for placeholder IPC,
        # should be refined to more specific exceptions in production.
        logging.error("Error sending command to agent: %s", err)
        # pylint: disable=W1404 # For some reason, pylint still flags this f-string
        return {"error": f"IPC communication error: {err}"}


def start_ipc_server(handler_function):
    """
    Starts an IPC server (Unix Domain Socket) for the agent to listen for
    commands. The handler_function will be called with the parsed command
    dictionary.
    """
    if os.path.exists(UDS_PATH):
        try:
            os.remove(UDS_PATH)  # Clean up previous socket if it exists
        except OSError as err:
            logging.error("Error removing old UDS socket %s: %s", UDS_PATH, err)
            # If we can't remove, maybe another process holds it. Exit.
            raise

    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(UDS_PATH)
    server_socket.listen(1)  # Listen for one incoming connection
    logging.info("IPC server listening on %s", UDS_PATH)

    try:
        while True:
            conn, _ = server_socket.accept()
            try:
                data = conn.recv(4096).decode("utf-8")
                command_dict = json.loads(data)

                # Process command using the provided handler function
                response = handler_function(command_dict)

                conn.sendall(json.dumps(response).encode("utf-8"))
            except Exception as err:  # pylint: disable=broad-exception-caught
                # Catching broad exception for now for placeholder IPC,
                # should be refined to more specific exceptions in production.
                logging.error("Error processing IPC command: %s", err)
                conn.sendall(json.dumps({"error": str(err)}).encode("utf-8"))
            finally:
                conn.close()
    except KeyboardInterrupt:
        logging.info("IPC server shutting down.")
    finally:
        server_socket.close()
        if os.path.exists(UDS_PATH):
            os.remove(UDS_PATH)  # Clean up socket on exit


# Example handler for agent core
def agent_command_handler(command_dict):
    """
    Placeholder function to handle incoming commands for the agent core.
    """
    command = command_dict.get("command")
    # Pylint R1705: Unnecessary "elif" after "return"
    # Changed to if/return statements directly
    if command == "status":
        return {"status": "Agent is running", "uptime": "X hours"}
    if command == "reload_config":
        return {"status": "Config reloaded"}
    if command == "stop_daemon":  # Added for CLI to stop agent
        # In a real daemon, this would signal the main loop to exit
        # import agent_core
        # agent_core.AGENT_RUNNING = False
        return {"status": "Stop command received"}
    return {"error": f"Unknown command: {command}"}


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    # Example of how to start the IPC server
    # start_ipc_server(agent_command_handler)
    logging.info("IPC module. Run agent_core.py to start daemon with IPC server.")
