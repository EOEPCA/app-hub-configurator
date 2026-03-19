from click.testing import CliRunner

from configurator.main import main
from tests.helpers import read_yaml


PLUGIN_DIR = "data/work/extra-profiles"


def test_eoepca_coder_profile_includes_copy_secrets(tmp_path):
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles-dir",
            PLUGIN_DIR,
            "--profiles",
            "eoepca_coder_app",
            "--groups",
            "group-a",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output

    config = read_yaml(output)
    profile = config["profiles"][0]

    assert profile["definition"]["slug"] == "eoepca_coder_app"
    assert profile["image_pull_secrets"][0]["name"] == "incluster-cr-secret"
    assert any(cm["name"] == "copy-secrets-eoepca-coder-app" for cm in profile["config_maps"])
    assert profile["pod_env_vars"]["NAMESPACE"] == "{{ namespace }}"
