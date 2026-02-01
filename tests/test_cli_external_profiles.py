from click.testing import CliRunner

from configurator.main import main
from tests.helpers import read_yaml, get_slugs


def test_profiles_dir_external_profile(tmp_path):
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()

    # external module registers a profile into registry
    (plugin_dir / "external_profiles.py").write_text(
        """
from configurator.apps import profile_registry
from configurator.apps.base import BaseAppProfile

class ExternalProfile(BaseAppProfile):
    slug = "external_profile"
    display_name = "External Profile"
    description = "Loaded from --profiles-dir"
    image = "alpine:3.19"

profile_registry.register(ExternalProfile)
"""
    )

    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles-dir",
            str(plugin_dir),
            "--profiles",
            "external_profile",
            "--groups",
            "group-a",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output

    config = read_yaml(output)
    assert get_slugs(config) == ["external_profile"]
