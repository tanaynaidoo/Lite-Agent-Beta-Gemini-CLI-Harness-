# Contributing to Lite-Agent-Beta-Gemini-CLI-Harness

We welcome contributions to the `Lite-Agent-Beta-Gemini-CLI-Harness` project! Your help is invaluable in making this a robust and effective tool for AI agent development.

Please take a moment to review this document to understand our contribution guidelines.

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### 1. Fork the Repository

First, fork the `Lite-Agent-Beta-Gemini-CLI-Harness` repository to your GitHub account.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/Lite-Agent-Beta-Gemini-CLI-Harness-
cd Lite-Agent-Beta-Gemini-CLI-Harness-
```
Replace `YOUR_USERNAME` with your GitHub username.

### 3. Set up the Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Pre-commit Hooks

Our project uses `pre-commit` hooks to ensure code quality and consistency. Please install them:

```bash
pre-commit install
```
These hooks will automatically run `black` (formatter), `isort` (import sorter), `flake8` (linter), `pylint` (static analyzer), and `pytest` (test runner) on your staged changes before each commit.

### 6. Create a New Branch

Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name # For new features
# or
git checkout -b bugfix/issue-description # For bug fixes
```

### 7. Make Your Changes

*   Implement your feature or bug fix.
*   Write clear, concise, and well-documented code.
*   Ensure your changes adhere to the existing code style.

### 8. Write Tests

*   **All new features must be accompanied by tests.**
*   **All bug fixes should include a test that demonstrates the fix.**
*   Run the test suite to ensure no existing functionality is broken:

    ```bash
    pytest
    ```

### 9. Run Code Quality Checks

While pre-commit hooks will run automatically, you can run them manually to catch issues early:

```bash
source .venv/bin/activate
black .
isort .
flake8 .
pylint --rcfile=.pylintrc src tests
```

### 10. Commit Your Changes

Commit your changes with a clear and descriptive commit message. Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification if possible (e.g., `feat: Add new feature`, `fix: Resolve bug in X`).

```bash
git add .
git commit -m "feat: Briefly describe your changes"
```

### 11. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 12. Create a Pull Request (PR)

1.  Go to the original `Lite-Agent-Beta-Gemini-CLI-Harness` repository on GitHub.
2.  Click on the "Compare & pull request" button.
3.  Provide a clear title and description for your PR, explaining the changes and why they are necessary.
4.  Ensure all CI checks pass.
5.  Request a review.

## Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style, enforced by `black`, `flake8`, `isort`, and `pylint`.

## Reporting Bugs

If you find a bug, please open an issue on GitHub and provide as much detail as possible, including:

*   Steps to reproduce the bug.
*   Expected behavior.
*   Actual behavior.
*   Your operating system and Python version.

## Feature Requests

Feel free to open an issue to suggest new features or improvements.

Thank you for contributing!
