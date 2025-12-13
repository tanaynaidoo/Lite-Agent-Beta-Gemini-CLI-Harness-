# src/lite_agent/agent_core.py
"""
Core logic for the Lite Agent daemon.

This module contains the main loop, task execution, and daemonization logic
for the Lite Agent.
"""

import logging
import os
import signal
import sys
import time

# Import IPC functions from local module
# pylint: disable=W0611 # UDS_PATH is not directly used in this file
from .ipc import UDS_PATH, agent_command_handler, start_ipc_server

# Global flag to control agent's running state
# pylint: disable=C0103 # AGENT_RUNNING is a constant.
AGENT_RUNNING = (
    True  # pylint: disable=W0603 # Global statement needed for signal handler
)
PID_FILE = "/tmp/lite_agent.pid"  # Define PID file path


def _daemonize():
    """
    Standard UNIX double-fork magic for daemonization.
    """
    try:
        pid = os.fork()
        if pid > 0:
            # Exit first parent
            sys.exit(0)
    except OSError as e:
        logging.error("Fork #1 failed: %d (%s)", e.errno, e.strerror)
        sys.exit(1)

    # Decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            # Exit second parent
            sys.exit(0)
    except OSError as e:
        logging.error("Fork #2 failed: %d (%s)", e.errno, e.strerror)
        sys.exit(1)

    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    # Pylint W1514: Using open without explicitly specifying an encoding
    # Pylint R1732: Consider using 'with' for resource-allocating operations
    with open(os.devnull, "r", encoding="utf-8") as si:
        with open(os.devnull, "a+", encoding="utf-8") as so:
            with open(os.devnull, "a+", encoding="utf-8") as se:
                os.dup2(si.fileno(), sys.stdin.fileno())
                os.dup2(so.fileno(), sys.stdout.fileno())
                os.dup2(se.fileno(), sys.stderr.fileno())

    # Write PID file
    # Pylint W1514: Using open without explicitly specifying an encoding
    # Pylint R1732: Consider using 'with' for resource-allocating operations
    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, _handle_sigterm)
    signal.signal(signal.SIGHUP, _handle_sighup)  # Example for config reload


def _handle_sigterm(signum, frame):  # pylint: disable=unused-argument
    """
    Signal handler for SIGTERM to gracefully stop the agent.
    """
    global AGENT_RUNNING  # pylint: disable=W0603 # Global statement needed for signal handler
    logging.info("SIGTERM received. Shutting down agent gracefully...")
    AGENT_RUNNING = False
    _cleanup_pid_file()
    sys.exit(0)


def _handle_sighup(signum, frame):  # pylint: disable=unused-argument
    """
    Signal handler for SIGHUP (e.g., to reload configuration).
    """
    logging.info("SIGHUP received. Reloading configuration (placeholder)...")
    # Add logic to reload configuration here


def _cleanup_pid_file():
    """
    Removes the PID file.
    """
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
        logging.info("PID file %s removed.", PID_FILE)


def run_agent_tasks():
    """
    Placeholder for the agent's background tasks.
    This would run in a separate thread/process in a real implementation.
    """
    global AGENT_RUNNING  # pylint: disable=W0603 # Global statement needed for signal handler
    while AGENT_RUNNING:
        logging.debug("Agent is alive, performing background tasks...")
        # Add actual agent logic here (monitoring, data processing, etc.)
        time.sleep(5)


def start_daemon():
    """
    Handles daemonization and starts the agent's main loop and IPC server.
    """
    global AGENT_RUNNING  # pylint: disable=W0603 # Global statement needed for signal handler
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Lite Agent daemonization initiated.")

    # Only daemonize if not already in daemon mode (e.g., if called directly)
    if os.getpid() != os.setsid():  # Simple check if already a session leader
        _daemonize()

    # Once daemonized, logging needs to be re-initialized if redirected to a file
    # For now, it logs to /dev/null, but this would be a file in production.
    # logging.basicConfig(level=logging.INFO, filename='/var/log/lite_agent.log', ...)

    logging.info("Starting IPC server...")
    # The IPC server will block until SIGTERM or KeyboardInterrupt
    start_ipc_server(agent_command_handler)

    # After IPC server exits (e.g., due to SIGTERM), perform cleanup
    _cleanup_pid_file()
    logging.info("Lite Agent daemon stopped.")


if __name__ == "__main__":
    start_daemon()
