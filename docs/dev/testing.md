# Testing

Configurator uses `pytest` and `click.testing.CliRunner`.

Most tests execute the CLI and validate the generated YAML rather than testing internals in isolation.

## Running tests

If you use Hatch:

```bash
hatch run test:test-q
```

Available scripts from `pyproject.toml`:

- `hatch run test:test`
- `hatch run test:test-q`
- `hatch run test:test-cov`
- `hatch run test:test-show-setup`

If you use the task runner:

```bash
task test
```

That task currently runs `hatch run test:test-show-setup`.

## Test structure

Current coverage is organized around:

- CLI generation: `tests/test_cli_dump_config.py`
- overrides and node selectors: `tests/test_cli_overrides.py`
- CLI failures and validation errors: `tests/test_cli_failures.py`
- listing and describing profiles: `tests/test_cli_list_describe.py`
- structured manifest dumping: `tests/test_cli_manifests_dumping.py`
- external plugin loading: `tests/test_cli_external_profiles.py` and `tests/test_external_profiles.py`
- registry behavior: `tests/test_registry.py`

## Test patterns

Common pattern:

1. use `CliRunner`
2. invoke `configurator.main.main`
3. write output to a temporary file
4. parse YAML with test helpers
5. assert on generated structure

Example:

```python
from click.testing import CliRunner

from configurator.main import main


def test_list_profiles():
    runner = CliRunner()
    result = runner.invoke(main, ["--list-profiles"])

    assert result.exit_code == 0
    assert "coder_app" in result.output
```

## Registry isolation

The suite uses autouse fixtures in `tests/conftest.py` to clear the global `profile_registry` between tests.

That matters because:

- built-in profiles register at import time
- plugin tests import external modules dynamically
- duplicate registrations would otherwise leak across tests

## When adding tests

For a new profile or feature, prefer adding tests that exercise user-visible behavior:

- successful config generation
- override handling
- failure messages for invalid input
- manifest structure when YAML documents are involved

This keeps the suite aligned with the CLI contract.
