from click.testing import CliRunner

from configurator.main import main
from tests.helpers import read_yaml, get_slugs


def test_dump_config_multiple_profiles(tmp_path):
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles",
            (
                "coder_app,gpu_coder_app,remote_desktop,qgis_remote_desktop,"
                "panoply_remote_desktop,snap_remote_desktop,coder_dask_gateway_app,"
                "training_how_to_app"
            ),
            "--groups",
            "group-a,group-b,group-c",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output
    assert output.exists()

    config = read_yaml(output)
    assert "profiles" in config
    assert len(config["profiles"]) == 8

    slugs = get_slugs(config)
    assert "coder_app" in slugs
    assert "gpu_coder_app" in slugs
    assert "remote_desktop" in slugs
    assert "coder_dask_gateway_app" in slugs
