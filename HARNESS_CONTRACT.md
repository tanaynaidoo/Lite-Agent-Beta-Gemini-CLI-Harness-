# HARNESS_CONTRACT.md

## The Prime Directive (Non-Negotiable)
> **Git is the definitive source of truth for the project's source code, build scripts, and default/template configurations.**
>
> The repository must never mutate its committed source code or default configuration implicitly. Runtime configuration and operational state are managed separately and dynamically.

## Immutable Rules

*   **Generated `.py` files:** If `.py` files are generated, their generation must be deterministic, driven by version-controlled source artifacts (e.g., IDL, schema, configuration), and the generator script itself must be version-controlled. Generated `.py` files should either be committed to the repository (if part of the deliverable and needed for static analysis/IDE support) or reliably generated as part of the project's build/install process. Dynamic generation of `.py` at *runtime* for execution is prohibited.
*   No hardcoded workspace paths; paths must be resolved dynamically or relative to the project root.
*   No background daemon without explicit CLI invocation (`esl-harness <command>`).
*   `doctor` command must always be truthful and reflect the actual operational health.
*   Git state must fully define the buildable and deployable project; any deviations must be explicitly managed by user actions or documented external factors.

## Allowed Changes

*   New commands
*   New tests
*   New host adapters under `/host`
*   Refinements to generated `.py` rules (e.g., specific schemas and generators).
*   Updates to documentation reflecting operational guidelines or environmental specifics.
*   Creation and maintenance of platform-specific build processes and installer scripts (e.g., PyInstaller, NSIS, Inno Setup, `.deb`, `.rpm` packages) within designated `host/` or `build/` directories.

## Forbidden Forever

*   Implicit mutation of committed source code or default configuration.
*   Silent modification of project files without explicit user action or version control.
*   Ad-hoc, undocumented, or unversioned OS-specific Python logic that impedes cross-platform consistency. OS-specific logic should be abstracted, confined to host adapters, or clearly managed via platform detection within CLI/installation logic.
*   Directly committing sensitive runtime configuration (e.g., API keys, private credentials) to Git.
