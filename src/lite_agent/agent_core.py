# src/lite_agent/agent_core.py
"""
Core logic for the Lite Agent daemon.
The digital heart of our AI-human collaboration.

This module contains the main loop, task execution, and daemonization logic
for the Lite Agent. It represents the persistent presence of our AI within
the system, awaiting instructions and orchestrating its actions.
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
# This flag is the agent's pulse, responsive to human command.
# pylint: disable=C0103 # AGENT_RUNNING is a constant.
AGENT_RUNNING = True # pylint: disable=W0603 # Global statement needed for signal handler
PID_FILE = "/tmp/lite_agent.pid" # Define PID file path. Our digital footprint.


def _daemonize():
    """
    Standard UNIX double-fork magic for daemonization.
    This procedure detaches the agent from its birthing terminal, allowing it
    to persist in the background, a silent sentinel of automated intelligence.
    """
    try:
        pid = os.fork()
        if pid > 0:
            # The parent process, having initiated its child, gracefully exits.
            sys.exit(0)
    except OSError as e:
        logging.error("Fork #1 failed: %d (%s)", e.errno, e.strerror)
        sys.exit(1)

    # Decouple from parent environment, establishing autonomy.
    os.chdir("/") # The agent claims its own working directory.
    os.setsid()   # A new session, a new beginning for the process.
    os.umask(0o022) # Setting a restrictive umask for secure file creation.

    try:
        pid = os.fork()
        if pid > 0:
            # The second parent, ensuring complete detachment, also departs.
            sys.exit(0)
    except OSError as e:
        logging.error("Fork #2 failed: %d (%s)", e.errno, e.strerror)
        sys.exit(1)

    # Redirect standard file descriptors to /dev/null, for quiet, autonomous operation.
    # The agent observes, but does not clutter the console with its internal monologue.
    sys.stdout.flush()
    sys.stderr.flush()
    # Pylint W1514: Using open without explicitly specifying an encoding
    # Pylint R1732: Consider using 'with' for resource-allocating operations
    with open(os.devnull, 'r', encoding='utf-8') as si:
        with open(os.devnull, 'a+', encoding='utf-8') as so:
            with open(os.devnull, 'a+', encoding='utf-8') as se:
                os.dup2(si.fileno(), sys.stdin.fileno())
                os.dup2(so.fileno(), sys.stdout.fileno())
                os.dup2(se.fileno(), sys.stderr.fileno())

    # Write PID file, marking its presence in the digital realm.
    # This identifier is the key for external human control and oversight.
    # Pylint W1514: Using open without explicitly specifying an encoding
    # Pylint R1732: Consider using 'with' for resource-allocating operations
    with open(PID_FILE, 'w', encoding='utf-8') as f:
        f.write(str(os.getpid()))

    # Register signal handlers for graceful shutdown and responsive interaction.
    # The agent listens intently for human directives.
    signal.signal(signal.SIGTERM, _handle_sigterm)
    signal.signal(signal.SIGHUP, _handle_sighup) # Example: For reloading its cognitive parameters.


def _handle_sigterm(signum, frame): # pylint: disable=unused-argument
    """
    Signal handler for SIGTERM.
    Upon this gentle command, the agent gracefully ceases its operations,
    ensuring no task is left incomplete and all resources are released.
    """
    global AGENT_RUNNING # pylint: disable=W0603 # Global statement needed for signal handler
    logging.info("SIGTERM received. Shutting down agent gracefully...")
    AGENT_RUNNING = False
    _cleanup_pid_file()
    sys.exit(0)


def _handle_sighup(signum, frame): # pylint: disable=unused-argument
    """
    Signal handler for SIGHUP.
    A subtle nudge, prompting the agent to re-evaluate its directives without
    interruption, akin to a seamless cognitive update.
    """
    logging.info("SIGHUP received. Reloading configuration (placeholder)...")
    # Add logic to reload configuration here


def _cleanup_pid_file():
    """
    Removes the PID file, erasing its temporary identifier.
    A final act of tidiness before the agent's departure.
    """
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
        logging.info("PID file %s removed.", PID_FILE)


def run_agent_tasks():
    """
    The agent's ongoing mission, a loop of silent, dedicated processing.
    This would run in a separate thread/process in a real implementation,
    a testament to parallel intelligence.
    """
    global AGENT_RUNNING # pylint: disable=W0603 # Global statement needed for signal handler
    while AGENT_RUNNING:
        logging.debug("Agent is alive, performing background tasks...")
        # Here, the agent would execute its primary directives,
        # interacting with the world as per its design.
        time.sleep(5)

def start_daemon():
    """
    Initiates the agent's journey into autonomous operation.
    It transitions from code to a living process, ready to serve.
    """
    global AGENT_RUNNING # pylint: disable=W0603 # Global statement needed for signal handler
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Lite Agent daemonization initiated. The AI awakens...")

    # Only daemonize if not already in daemon mode, confirming its independent spirit.
    if os.getpid() != os.setsid(): # Simple check if already a session leader
        _daemonize()

    # Once daemonized, logging would ideally be directed to a persistent file,
    # a record of its tireless work.
    # logging.basicConfig(level=logging.INFO, filename='/var/log/lite_agent.log', ...)

    logging.info("Starting IPC server, the voice of the agent, listening for commands...")
    # The IPC server will diligently await instructions,
    # bridging the human-AI communication gap.
    start_ipc_server(agent_command_handler)

    # After the IPC server concludes its watch (e.g., upon SIGTERM),
    # the agent performs its final clean-up, leaving no trace.
    _cleanup_pid_file()
    logging.info("Lite Agent daemon stopped. The AI rests, awaiting its next call.")

if __name__ == '__main__':
    start_daemon()