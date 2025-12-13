# Lite-Agent-Beta-Gemini-CLI-Harness: Project Roadmap

This document outlines the vision, current status, and future direction of the `Lite-Agent-Beta-Gemini-CLI-Harness` project. Our goal is to create a robust, extensible, and user-friendly framework for developing and deploying AI agents, particularly those leveraging powerful models like Google Gemini, with seamless CLI control.

## Vision

To empower developers to build production-ready AI agents with confidence, providing a solid foundation for daemonization, IPC, task execution, and intuitive command-line interaction, fostering a vibrant community around agent development.

## Current Status (MVP: Minimal Viable Product - Initial Framework)

We have established a strong foundational framework, ready for active development:

*   **Project Structure:** Modular and scalable Python project layout (`src`, `tests`, `docs`).
*   **Development Workflow:** Integrated `pre-commit` hooks for automated code quality (formatting, linting, testing) and GitHub Actions for Continuous Integration.
*   **Basic Daemonization:** Placeholder for agent daemonization logic including double-forking and PID file management.
*   **Basic IPC:** Placeholder for Unix Domain Socket (UDS) based Inter-Process Communication between CLI and agent core.
*   **CLI Structure:** `Click`-based CLI with placeholder `start`, `stop`, `status`, and `config` commands.
*   **Documentation:** Comprehensive `README.md`, `CONTRIBUTING.md`, and initial design reports.
*   **Containerization:** Basic `Dockerfile` for environment consistency.
*   **License:** MIT License for open-source collaboration.

## Planned Features & Future Milestones

This roadmap is subject to change based on community feedback, technological advancements, and project priorities.

### Phase 1: Core Agent Functionality (Next Steps)

*   **Robust Daemon Management:**
    *   Implement `python-daemon` library for more robust and portable daemonization.
    *   Refine PID file handling, including lock files.
    *   Implement proper logging to a file (`/var/log/lite_agent.log` or configurable).
*   **IPC Refinement:**
    *   Implement a robust IPC request/response mechanism for various agent commands.
    *   Error handling and timeouts for IPC communications.
    *   Structured IPC messages (e.g., JSON schema validation).
*   **Agent Core Loop:**
    *   Develop a basic, extensible agent main loop in `agent_core.py` to handle background tasks.
    *   Implement graceful shutdown logic for agent tasks.
*   **CLI Enhancement:**
    *   Implement actual `config get/set/show` commands, persisting configuration to a file (e.g., INI, YAML).
    *   Add `reload` command to trigger agent config reload via IPC.
    *   Refine CLI output with colors and better formatting (e.g., using `Rich`).

### Phase 2: Extensibility & Agent Tasks

*   **Pluggable Task System:** Design and implement a plugin architecture for adding new agent tasks dynamically.
*   **Example Agent Task:** Develop a simple, illustrative agent task (e.g., system resource monitoring, file watcher).
*   **Testing Utilities:** Provide helper functions and patterns for testing agent tasks.
*   **Advanced CLI Features:**
    *   Context-aware tab-completion.
    *   Interactive prompts for complex commands.
    *   Structured output options (`--format json`).

### Phase 3: Deployment & Community Tools

*   **System Service Integration:** Provide `systemd` unit file examples for easy deployment as a background service.
*   **Packaging:** Prepare for distribution via `pip` (PyPI).
*   **Extended Documentation:** Comprehensive API docs, tutorials, and use-case examples.
*   **Community Contributions:** Actively engage with contributors, review PRs, and maintain a welcoming environment.

## "Good First Issues" for Contributors

These issues are designed to be relatively straightforward and are excellent starting points for new contributors to get familiar with the codebase. They will be opened as GitHub Issues soon.

*   **Implement a simple "Hello World" agent task:** A background task that periodically logs "Hello from Agent!"
*   **Add a basic configuration file loader:** For `agent_core.py` to load initial settings.
*   **Enhance CLI output with colors:** Use `Click`'s styling or `Rich` to make CLI responses more readable.
*   **Refactor CLI `config` commands:** Implement basic read/write to a dummy config file.
*   **Create a basic `health` command:** For the CLI to query basic agent health (e.g., "IPC connection OK").

Join us in building the future of AI agent development!

---
