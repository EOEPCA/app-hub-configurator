# Developer onboarding

This guide is for engineers adding or changing profile behavior.

## 1. Local setup

From repository root:

```bash
pip install hatch
hatch env create
```

Sanity check:

```bash
hatch run dump-config --help
```

## 2. Know the project layout

Start with:

- `configurator/apps/` for profile families and concrete profiles
- `configurator/cli/` for command-line behavior
- `configurator/plugins/` for external profile loading
- `tests/` for CLI and registry behavior coverage

## 3. Daily developer commands

```bash
task check
task test
task lint
```

## 4. Typical change flow

1. Add or modify profile code.
2. Update tests in `tests/`.
3. Update docs under `docs/` when behavior changes.
4. Run checks and tests locally.
5. Open a pull request.

## 5. Recommended first reads

- `docs/dev/architecture.md`
- `docs/dev/adding-profiles.md`
- `docs/dev/testing.md`

