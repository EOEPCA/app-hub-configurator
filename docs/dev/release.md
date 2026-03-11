# Release

This repository is packaged with Hatch and publishes a wheel built from the local source tree.

## Version source

The project version is defined in:

- `configurator/__about__.py`

`pyproject.toml` reads that file through:

```toml
[tool.hatch.version]
path = "configurator/__about__.py"
```

## Recommended release workflow

1. Update `configurator/__about__.py`.
2. Run tests.
3. Run formatting and checks.
4. Build the distribution artifacts.
5. Validate the generated wheel in a clean environment or container.
6. Tag the release in Git.
7. Publish using your internal delivery process.

## Useful commands

Run tests:

```bash
hatch run test:test-q
```

Run checks:

```bash
hatch run dev:lint
hatch run dev:check
```

Build docs:

```bash
hatch run docs:build
```

Build the wheel:

```bash
hatch build -t wheel
```

Build the container image that installs the wheel:

```bash
docker build -t application-hub-configurator .
```

## Notes

- the Dockerfile builds a wheel in a builder stage and installs that wheel in the runtime stage
- there is no release automation documented in this repository beyond the local Hatch and Docker workflows
- if you add CI-based publishing later, update this document to describe the exact registry and tagging rules
