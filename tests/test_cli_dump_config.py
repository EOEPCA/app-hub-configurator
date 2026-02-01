from pathlib import Path

import yaml
from click.testing import CliRunner

from configurator.main import main


def test_dump_config_generates_yaml(tmp_path: Path):
    runner = CliRunner()

    out = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles",
            "coder_app,gpu_coder_app,remote_desktop,qgis_remote_desktop,panoply_remote_desktop,snap_remote_desktop,coder_dask_gateway_app,training_how_to_app",
            "--groups",
            "group-a,group-b,group-c",
            "--output",
            str(out),
        ],
    )

    # CLI should succeed
    assert result.exit_code == 0, result.output

    # output file should exist
    assert out.exists()

    # YAML should be valid
    config = yaml.safe_load(out.read_text())

    assert "profiles" in config
    assert isinstance(config["profiles"], list)
    assert len(config["profiles"]) == 8

    # ensure slugs exist
    slugs = [p["definition"]["slug"] for p in config["profiles"]]
    assert set(slugs) == {
        "coder_app",
        "gpu_coder_app",
        "remote_desktop",
        "qgis_remote_desktop",
        "panoply_remote_desktop",
        "snap_remote_desktop",
        "coder_dask_gateway_app",
        "training_how_to_app",
    }


def test_list_profiles():
    runner = CliRunner()

    result = runner.invoke(main, ["--list-profiles"])

    assert result.exit_code == 0
    assert "Available profiles:" in result.output
    assert "coder_app" in result.output


def test_describe_profile():
    runner = CliRunner()

    result = runner.invoke(main, ["--describe-profile", "coder_app"])

    assert result.exit_code == 0
    assert "Profile: coder_app" in result.output
    assert "Resources:" in result.output


def test_dump_config_multiple_profiles(tmp_path):
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles",
            "coder_app,gpu_coder_app,remote_desktop,qgis_remote_desktop,panoply_remote_desktop,snap_remote_desktop,coder_dask_gateway_app,training_how_to_app",
            "--groups",
            "group-a,group-b,group-c",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output
    assert output.exists()

    config = yaml.safe_load(output.read_text())
    assert "profiles" in config
    assert len(config["profiles"]) == 8

    slugs = [p["definition"]["slug"] for p in config["profiles"]]
    assert "coder_app" in slugs
    assert "gpu_coder_app" in slugs
    assert "remote_desktop" in slugs


def test_profiles_dir_plugin(tmp_path):
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()

    # create external profile module
    (plugin_dir / "my_profiles.py").write_text(
        """
from configurator.apps import profile_registry
from configurator.apps.base import BaseAppProfile

class ExtraProfile(BaseAppProfile):
    slug = "extra_profile"
    display_name = "Extra Profile"
    description = "External plugin profile"
    image = "alpine:3.19"

profile_registry.register(ExtraProfile)
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
            "extra_profile",
            "--groups",
            "group-a",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output

    config = yaml.safe_load(output.read_text())
    slugs = [p["definition"]["slug"] for p in config["profiles"]]
    assert slugs == ["extra_profile"]
