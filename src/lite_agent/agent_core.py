# src/lite_agent/agent_core.py
"""
Core logic for the Lite Agent daemon.

This module contains the main loop, task execution, and daemonization logic
for the Lite Agent.
"""

import logging
import time

# Import IPC functions from local module
from .ipc import agent_command_handler, start_ipc_server

# Global flag to control agent's running state
# pylint: disable=C0103,W0602 # C0103: `AGENT_RUNNING` is a constant.
# W0602: `AGENT_RUNNING` is meant to be global
# and modified by other parts of the agent,
# even if not explicitly assigned here.
AGENT_RUNNING = True


def run_agent_tasks():
    """
    Placeholder for the agent's background tasks.
    This would run in a separate thread/process in a real implementation.
    """
    global AGENT_RUNNING
    while AGENT_RUNNING:
        logging.debug("Agent is alive, performing background tasks...")
        # Add actual agent logic here (monitoring, data processing, etc.)
        time.sleep(5)


def start_daemon():
    """
    Handles daemonization and starts the agent's main loop and IPC server.
    """
    global AGENT_RUNNING
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Lite Agent daemonization initiated.")

    # In a real daemon, you'd daemonize here (e.g., with python-daemon library)
    # For this placeholder, we'll start the IPC server directly

    # Placeholder for starting agent background tasks (if any)
    # in a separate thread
    # agent_task_thread = threading.Thread(target=run_agent_tasks)
    # agent_task_thread.start()

    logging.info("Starting IPC server...")
    start_ipc_server(agent_command_handler)

    # In a real daemon, you'd also handle agent_task_thread.join()
    # or similar shutdown. For this simple placeholder, AGENT_RUNNING
    # might be set to False by an IPC command to gracefully exit
    # start_ipc_server.


if __name__ == "__main__":
    start_daemon()
