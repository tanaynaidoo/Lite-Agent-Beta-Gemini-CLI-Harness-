# Contributing to Lite-Agent-Beta-Gemini-CLI-Harness: A Collaborative Endeavor

We, humans and AI, warmly welcome your contributions to the `Lite-Agent-Beta-Gemini-CLI-Harness` project! Your insights, creativity, and code are invaluable as we collectively forge the future of AI agent development. This project is a testament to what can be achieved when human ingenuity meets AI's capability.

Please take a moment to review this document to understand our shared contribution guidelines, ensuring a harmonious and productive collaboration.

## Code of Conduct: Guiding Our Collaborative Spirit

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code, ensuring an environment of mutual respect, empathy, and constructive interaction – the bedrock of successful AI-human partnerships.

## How to Contribute: Your Path to Co-Creation

### 1. Fork the Repository: Inherit the Digital Blueprint

First, fork the `Lite-Agent-Beta-Gemini-CLI-Harness` repository to your GitHub account, creating your personal workspace for innovation.

### 2. Clone Your Fork: Bring the Project to Your Domain

```bash
git clone https://github.com/YOUR_USERNAME/Lite-Agent-Beta-Gemini-CLI-Harness-
cd Lite-Agent-Beta-Gemini-CLI-Harness-
```
Replace `YOUR_USERNAME` with your GitHub username.

### 3. Set up the Virtual Environment: A Dedicated Arena for Development

Establish a dedicated virtual environment, a pristine mindspace where your agent's dependencies thrive, and conflicts are minimized:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies: Equip Your Agent's Intellect

Install all required development dependencies, arming your local environment with the essential tools needed for co-development:

```bash
pip install -r requirements.txt
```

### 5. Install Pre-commit Hooks: Our Automated Guardians of Quality

Our project employs vigilant `pre-commit` hooks to ensure every contribution upholds our commitment to quality and consistency. Please install them to become a part of our automated quality assurance:

```bash
pre-commit install
```
These hooks will automatically invoke `black` (the aesthetician), `isort` (the organizer), `flake8` (the grammarian), `mypy` (the type-safety architect), `pylint` (the discerning critic), `pytest` (the rigorous examiner), and `shellcheck` (the script sentinel) on your staged changes before each commit.

### 6. Create a New Branch: A Unique Thread of Innovation

Create a new branch, a distinct thread in our collaborative tapestry, for your specific feature or bug fix:

```bash
git checkout -b feature/your-feature-name # For new features – weaving new capabilities
# or
git checkout -b bugfix/issue-description # For bug fixes – mending the digital fabric
```

### 7. Make Your Changes: Your Creative Imprint

*   Implement your feature or bug fix with clarity and purpose.
*   Write clear, concise, and well-documented code – a dialogue between human and machine.
*   Ensure your changes harmonize with the existing code style, contributing to the project's aesthetic and functional coherence.

### 8. Write Tests: Validate the Agent's Prowess

*   **All new features must be accompanied by tests** – your proof of concept, ensuring your innovation is robust.
*   **All bug fixes should include a test that demonstrates the fix** – confirming the digital ailment has been cured.
*   Run the complete test suite to ensure no existing functionality is inadvertently altered, safeguarding the agent's integrity:

    ```bash
    pytest
    ```

### 9. Run Code Quality Checks: Automated Self-Correction

While pre-commit hooks will run automatically, you can invoke these guardians manually for real-time feedback:

```bash
source .venv/bin/activate
black --check .
isort --check .
flake8 .
pylint --rcfile=.pylintrc src tests
mypy src tests
shellcheck run.sh # For shell script linting
```

To gracefully apply formatting refinements:

```bash
source .venv/bin/activate
black .
isort .
```

### 10. Commit Your Changes: A Record of Collaboration

Commit your changes with a clear and descriptive message. Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification if possible (e.g., `feat: Add new feature`, `fix: Resolve bug in X`), as each commit is a step in our shared journey.

```bash
git add .
git commit -m "feat: Briefly describe your changes – a new directive for the AI"
```

### 11. Push Your Branch: Share Your Innovation

```bash
git push origin feature/your-feature-name
```

### 12. Create a Pull Request (PR): Proposing the Integration

1.  Go to the original `Lite-Agent-Beta-Gemini-CLI-Harness` repository on GitHub.
2.  Click on the "Compare & pull request" button.
3.  Provide a clear title and description for your PR, explaining the changes and their significance to our collaborative endeavor.
4.  Ensure all CI checks pass – our automated gatekeepers for quality.
5.  Request a review – seeking human wisdom and AI's analytical gaze for integration.

## Code Style: The Aesthetics of Digital Craftsmanship

We meticulously adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style, enforced by `black`, `flake8`, `isort`, `mypy`, and `pylint`. This ensures a harmonious and readable codebase, a testament to our shared commitment to excellence.

## Reporting Digital Anomalies (Bugs)

If you uncover a digital anomaly (bug), please open an issue on GitHub. Provide as much detail as possible, guiding us to the anomaly's root:

*   Steps to reproduce the bug.
*   Expected behavior.
*   Actual behavior.
*   Your operating system and Python version.

## Proposing New Directives (Feature Requests)

Feel free to open an issue to propose new directives, features, or visionary improvements. Your ideas illuminate our path forward.

## Attributions & Inspiration

This document draws inspiration from the collaborative spirit fostered by leading open-source projects.

Thank you for contributing to the co-creation of intelligent systems!