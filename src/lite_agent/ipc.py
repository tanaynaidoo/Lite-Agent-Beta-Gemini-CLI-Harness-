# src/lite_agent/ipc.py
"""
Inter-Process Communication (IPC) mechanisms for the Lite Agent.

This module handles communication between the CLI and the running agent daemon.
It will primarily use Unix Domain Sockets for efficient and secure local communication.
"""

import json
import logging
import os
import signal  # Added for sending SIGTERM from CLI
import socket

# Removed unused import: import subprocess # pylint: disable=unused-import


# flake8: noqa: E501 (Ignoring line length for UDS_PATH definition if it gets long)

# Define the Unix Domain Socket path
# This should ideally be configurable and located in a secure, writable path
# For example, in /var/run/lite_agent.sock for system services,
# or a user-specific path in ~/.cache/lite_agent/lite_agent.sock
UDS_DIR = "/tmp/lite_agent_ipc"
UDS_PATH = os.path.join(UDS_DIR, "lite_agent.sock")
PID_FILE = "/tmp/lite_agent.pid"  # Re-use PID_FILE from agent_core


# pylint: disable=R0911 # Too many return statements for now, acceptable for IPC
def send_command_to_agent(command_dict):
    """
    Sends a command to the running Lite Agent daemon via Unix Domain Socket.
    """
    if not os.path.exists(UDS_PATH):
        logging.error("Agent socket not found at %s. Is the agent running?", UDS_PATH)
        # If UDS is not found, try to check PID file and signal for stop
        if command_dict.get("command") == "stop_daemon" and os.path.exists(PID_FILE):
            try:
                # pylint: disable=W1514,R1732
                with open(PID_FILE, "r", encoding="utf-8") as f:
                    pid = int(f.read().strip())
                logging.info("Sending SIGTERM to agent with PID %s...", pid)
                os.kill(pid, signal.SIGTERM)
                return {"status": "SIGTERM sent to agent."}
            except (ValueError, FileNotFoundError, OSError) as e:
                logging.error("Failed to send SIGTERM to PID %s: %s", pid, e)
                return {"error": f"Failed to stop agent: {e}"}
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
    except (socket.error, json.JSONDecodeError) as err:
        logging.error("Error sending command to agent: %s", err)
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

    # Create UDS directory if it doesn't exist and set permissions
    os.makedirs(UDS_DIR, mode=0o700, exist_ok=True)

    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(UDS_PATH)
    os.chmod(UDS_PATH, 0o600)  # Set strict permissions on the socket file
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
            except (socket.error, json.JSONDecodeError) as err:
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
        if os.path.exists(UDS_DIR):
            os.rmdir(UDS_DIR)  # Clean up socket directory on exit


# Example handler for agent core
def agent_command_handler(command_dict):
    """
    Placeholder function to handle incoming commands for the agent core.
    """
    command = command_dict.get("command")
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
    logging.info("IPC module. Run agent_core.py to start daemon with IPC server.")
