# src/lite_agent/ipc.py
"""
Inter-Process Communication (IPC) mechanisms for the Lite Agent.
The silent network, enabling human-AI dialogue.

This module handles communication between the CLI and the running agent daemon.
It serves as the vital link, translating human commands into the AI's language
and relaying the AI's responses back. It uses TCP sockets for efficient
and secure local communication.
"""

import json
import logging
import os
import signal  # Added for sending SIGTERM from CLI
import socket
import tempfile

# flake8: noqa: E501 (Ignoring line length for UDS_PATH definition if it gets long)

# Define the TCP socket parameters.
# This channel ensures reliable communication between human and AI.
IPC_HOST = "127.0.0.1"  # Localhost for security
IPC_PORT = 50000  # High-numbered port to avoid conflicts
PID_FILE = os.path.join(tempfile.gettempdir(), "lite_agent.pid")  # The AI's digital fingerprint.


# pylint: disable=R0911 # Too many return statements for now, acceptable for IPC
def send_command_to_agent(command_dict):
    """
    Sends a command to the running Lite Agent daemon via TCP socket.
    This is the human's voice, delivering commands to the AI's core.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IPC_HOST, IPC_PORT))

        message = json.dumps(command_dict)
        client_socket.sendall(message.encode("utf-8"))

        # Receive response from the AI
        response_data = client_socket.recv(4096).decode("utf-8")
        response_dict = json.loads(response_data)

        client_socket.close()
        return response_dict
    except ConnectionRefusedError:
        logging.error(
            "Connection refused. Agent might not be running or is unresponsive. "
            "The AI is momentarily unresponsive to queries."
        )
        if command_dict.get("command") == "stop_daemon" and os.path.exists(PID_FILE):
            try:
                with open(PID_FILE, "r", encoding="utf-8") as f:
                    pid = int(f.read().strip())
                logging.info("Sending SIGTERM to agent with PID %s... "
                             "A gentle request for the AI to cease operations.", pid)
                os.kill(pid, signal.SIGTERM)
                return {"status": "SIGTERM sent to agent."}
            except (ValueError, FileNotFoundError, OSError) as e:
                logging.error("Failed to send SIGTERM to PID %s: %s. "
                              "The AI resists, or is already beyond reach.", pid, e)
                return {"error": f"Failed to stop agent: {e}"}
        return {"error": "Agent not running or connection refused."}
    except (socket.error, json.JSONDecodeError) as err:
        logging.error("Error sending command to agent: %s. "
                      "A glitch in the human-AI matrix.", err)
        return {"error": f"IPC communication error: {err}"}


def start_ipc_server(handler_function):
    """
    Starts an IPC server (TCP socket) for the agent to listen for
    commands. This is the AI's listening ear, always attuned to human directives.
    The handler_function will be called with the parsed command dictionary.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IPC_HOST, IPC_PORT))
    server_socket.listen(1)  # Listen for one incoming connection, focused.
    logging.info("IPC server listening on %s:%s. The AI awaits instructions.", IPC_HOST, IPC_PORT)

    try:
        while True:
            conn, _ = server_socket.accept()
            try:
                data = conn.recv(4096).decode("utf-8")
                command_dict = json.loads(data)

                # Process command using the provided handler function.
                # The AI interprets human intent.
                response = handler_function(command_dict)

                conn.sendall(json.dumps(response).encode("utf-8"))
            except (socket.error, json.JSONDecodeError) as err:
                logging.error("Error processing IPC command: %s. "
                              "Miscommunication in the digital ether.", err)
                conn.sendall(json.dumps({"error": str(err)}).encode("utf-8"))
            finally:
                conn.close()
    except KeyboardInterrupt:
        logging.info("IPC server shutting down. The AI's ear closes.")
    finally:
        server_socket.close()


# Example handler for agent core
def agent_command_handler(command_dict):
    """
    Placeholder function to handle incoming commands for the agent core.
    This is where the AI's logic receives and processes the human's commands.
    """
    command = command_dict.get("command")
    if command == "status":
        return {"status": "Agent is running", "uptime": "X hours"}
    if command == "reload_config":
        return {"status": "Config reloaded"}
    if command == "stop_daemon":  # Added for CLI to stop agent
        # In a real daemon, this would signal the main loop to exit.
        # The AI processes the request for a graceful pause.
        # import agent_core
        # agent_core.AGENT_RUNNING = False
        return {"status": "Stop command received by IPC server."}
    return {"error": f"Unknown command: {command}. The AI does not comprehend."}


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("IPC module. The stage is set for AI-human interaction.")