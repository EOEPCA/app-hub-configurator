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
