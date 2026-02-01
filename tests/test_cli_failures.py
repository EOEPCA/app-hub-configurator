from click.testing import CliRunner

from configurator.main import main


def run_cli(args: list[str]):
    runner = CliRunner()
    return runner.invoke(main, args)


def test_unknown_profile_slug_fails():
    result = run_cli(
        [
            "--profiles",
            "does_not_exist",
            "--groups",
            "group-a",
        ]
    )

    assert result.exit_code != 0
    assert "Unknown profile slug" in result.output or "does_not_exist" in result.output


def test_invalid_override_format_missing_colon():
    result = run_cli(
        [
            "--profiles",
            "coder_app",
            "--groups",
            "group-a",
            "--override",
            "coder_app=cpu_limit=4",  # ❌ should be slug:field=value
        ]
    )

    assert result.exit_code != 0
    assert "Invalid --override" in result.output
    assert "Expected <slug>:<field>=<value>" in result.output


def test_invalid_override_format_missing_equals():
    result = run_cli(
        [
            "--profiles",
            "coder_app",
            "--groups",
            "group-a",
            "--override",
            "coder_app:cpu_limit",  # ❌ missing =value
        ]
    )

    assert result.exit_code != 0
    assert "Invalid --override" in result.output


def test_invalid_node_selector_format_missing_colon():
    result = run_cli(
        [
            "--profiles",
            "coder_app",
            "--groups",
            "group-a",
            "--node-selector",
            "coder_app=nodepool=gpu",  # ❌ should be slug:key=value
        ]
    )

    assert result.exit_code != 0
    assert "Invalid --node-selector" in result.output
    assert "Expected <slug>:<key>=<value>" in result.output


def test_invalid_node_selector_format_missing_equals():
    result = run_cli(
        [
            "--profiles",
            "coder_app",
            "--groups",
            "group-a",
            "--node-selector",
            "coder_app:nodepool",  # ❌ missing =value
        ]
    )

    assert result.exit_code != 0
    assert "Invalid --node-selector" in result.output


def test_empty_groups_fails():
    # groups option accepts CSV; empty should fail
    result = run_cli(
        [
            "--profiles",
            "coder_app",
            "--groups",
            "",  # will parse to []
        ]
    )

    assert result.exit_code != 0
    assert "At least one group must be specified" in result.output


def test_unknown_override_field_fails():
    result = run_cli(
        [
            "--profiles",
            "coder_app",
            "--groups",
            "group-a",
            "--override",
            "coder_app:does_not_exist=123",
        ]
    )

    assert result.exit_code != 0
    assert "Unknown override field" in result.output
    assert "does_not_exist" in result.output


def test_invalid_cpu_override_type_fails():
    result = run_cli(
        [
            "--profiles",
            "coder_app",
            "--groups",
            "group-a",
            "--override",
            "coder_app:cpu_limit=not_an_int",
        ]
    )

    assert result.exit_code != 0
    assert "invalid value for cpu_limit" in result.output.lower()
    assert "must be an integer" in result.output.lower()


def test_groups_override_empty_fails():
    result = run_cli(
        [
            "--profiles",
            "coder_app",
            "--groups",
            "group-a",
            "--override",
            "coder_app:groups=",  # override groups to empty
        ]
    )

    assert result.exit_code != 0
    assert "groups override for 'coder_app' cannot be empty" in result.output
