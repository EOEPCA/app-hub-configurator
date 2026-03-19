# Contributing

Thanks for your interest in contributing to `app-hub-configurator`.

## Getting started

1. Fork the repository and create a feature branch.
2. Set up the project tooling:
   - `pip install hatch`
3. Run checks locally:
   - `task test`
   - `task check`
   - `task lint`

## Development workflow

1. Keep changes focused and small.
2. Add or update tests for behavior changes.
3. Update docs when CLI behavior, defaults, or profile schema changes.
4. Ensure all checks pass before opening a pull request.

## Commit and pull request guidelines

1. Use clear commit messages.
2. Reference related issues in the PR description.
3. Describe:
   - what changed
   - why it changed
   - how it was tested
4. Include sample CLI output or YAML snippets when useful.

## Code style

- Python formatting and linting are enforced with Ruff.
- Prefer explicit, typed, and testable code paths.
- Avoid breaking CLI compatibility without discussion.

## Reporting issues

Use GitHub Issues and include:

- expected behavior
- actual behavior
- reproduction steps
- environment details (OS, Python version, command used)

