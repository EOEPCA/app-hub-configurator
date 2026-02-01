import textwrap
from click.testing import CliRunner

from configurator.main import main
from configurator.apps import profile_registry


def write_module(tmp_path, name: str, content: str):
    """
    Create <tmp_path>/<name>.py with provided content.
    """
    mod = tmp_path / f"{name}.py"
    mod.write_text(textwrap.dedent(content))
    return mod


def test_external_profiles_register_and_can_be_used(tmp_path):
    """
    Create an external module defining a profile and registering it.
    Then call CLI with --profiles-dir and use that slug.
    """
    # external module
    write_module(
        tmp_path,
        "my_profiles",
        """
        from configurator.apps import profile_registry
        from configurator.apps.base import BaseAppProfile

        class MyExternalProfile(BaseAppProfile):
            slug = "external_coder"
            display_name = "External Coder"
            description = "Coder from plugin folder"
            image = "ghcr.io/example/external:latest"

        profile_registry.register(MyExternalProfile)
        """,
    )

    runner = CliRunner()
    out = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles-dir",
            str(tmp_path),
            "--profiles",
            "external_coder",
            "--groups",
            "group-a",
            "--output",
            str(out),
        ],
    )

    assert result.exit_code == 0, result.output
    assert out.exists()

    # Ensure registry got populated
    assert profile_registry.get("external_coder").slug == "external_coder"


def test_external_profiles_not_loaded_without_profiles_dir(tmp_path):
    """
    Ensure that without --profiles-dir, the external slug is unknown.
    """
    write_module(
        tmp_path,
        "my_profiles",
        """
        from configurator.apps import profile_registry
        from configurator.apps.base import BaseAppProfile

        class MyExternalProfile(BaseAppProfile):
            slug = "external_coder"
            display_name = "External Coder"
            description = "Coder from plugin folder"
            image = "ghcr.io/example/external:latest"

        profile_registry.register(MyExternalProfile)
        """,
    )

    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            "--profiles",
            "external_coder",
            "--groups",
            "group-a",
        ],
    )

    assert result.exit_code != 0
    assert "Unknown profile slug" in result.output
    assert "external_coder" in result.output


def test_external_profiles_duplicate_slug_fails(tmp_path):
    """
    External profile tries to register an existing slug -> should fail.
    """
    write_module(
        tmp_path,
        "bad_profiles",
        """
        from configurator.apps import profile_registry
        from configurator.apps.base import BaseAppProfile

        class Duplicate(BaseAppProfile):
            slug = "coder_app"
            display_name = "Duplicate"
            description = "Should conflict"
            image = "dummy:latest"

        profile_registry.register(Duplicate)
        """,
    )

    runner = CliRunner()

    # Must ensure internal profiles are registered first
    import configurator.apps.coder  # noqa: F401

    result = runner.invoke(
        main,
        [
            "--profiles-dir",
            str(tmp_path),
            "--list-profiles",
        ],
    )

    assert result.exit_code != 0
    assert (
        "Duplicate profile slug" in result.output
        or "Duplicate profile slug" in repr(result.exception)
    )


def test_external_profiles_invalid_python_module_fails(tmp_path):
    """
    If external module has syntax error -> import fails.
    """
    write_module(
        tmp_path,
        "broken",
        """
        def this_is_invalid_python(
        """,
    )

    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            "--profiles-dir",
            str(tmp_path),
            "--list-profiles",
        ],
    )

    assert result.exit_code != 0
    # error message differs depending on python version
    assert (
        "SyntaxError" in repr(result.exception)
        or "invalid syntax" in str(result.exception).lower()
    )
