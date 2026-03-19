from click.testing import CliRunner

from configurator.main import main
from tests.helpers import read_yaml, get_slugs


PLUGIN_DIR = "data/work/extra-profiles"


def test_downstream_training_profile_requires_profiles_dir():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--profiles",
            "training_how_to_app",
            "--groups",
            "group-a",
        ],
    )

    assert result.exit_code != 0
    assert "Unknown profile slug" in result.output
    assert "training_how_to_app" in result.output


def test_downstream_profiles_are_available_with_profiles_dir(tmp_path):
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles-dir",
            PLUGIN_DIR,
            "--profiles",
            "training_how_to_app,mlflow_coder_app",
            "--groups",
            "group-a",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output

    config = read_yaml(output)
    assert get_slugs(config) == ["training_how_to_app", "mlflow_coder_app"]


def test_downstream_training_profile_can_be_described_with_profiles_dir():
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--profiles-dir",
            PLUGIN_DIR,
            "--describe-profile",
            "training_how_to_app",
        ],
    )

    assert result.exit_code == 0
    assert "Profile: training_how_to_app" in result.output
