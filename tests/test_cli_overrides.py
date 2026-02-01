from click.testing import CliRunner

from configurator.main import main
from tests.helpers import read_yaml


def test_override_cpu_limit(tmp_path):
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles",
            "coder_app",
            "--groups",
            "group-a",
            "--override",
            "coder_app:cpu_limit=9",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output

    config = read_yaml(output)
    profile = config["profiles"][0]
    override = profile["definition"]["kubespawner_override"]
    assert override["cpu_limit"] == 9


def test_node_selector_override(tmp_path):
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles",
            "gpu_coder_app",
            "--groups",
            "group-a",
            "--node-selector",
            "gpu_coder_app:nodepool=gpu",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output

    config = read_yaml(output)
    profile = config["profiles"][0]
    assert profile["node_selector"]["nodepool"] == "gpu"


def test_overide_image(tmp_path):
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles",
            "gpu_coder_app",
            "--groups",
            "group-a",
            "--override",
            "gpu_coder_app:image=ghcr.io/terradue/coder-gpu:latest",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output

    config = read_yaml(output)
    profile = config["profiles"][0]
    definition = profile["definition"]
    kube_override = definition["kubespawner_override"]
    assert kube_override["image"] == "ghcr.io/terradue/coder-gpu:latest"


def test_overridden_groups(tmp_path):
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles",
            "coder_app",
            "--groups",
            "group-a",
            "--override",
            "coder_app:groups=group-b,group-c",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output

    config = read_yaml(output)
    profile = config["profiles"][0]
    assert profile["groups"] == ["group-b", "group-c"]


def test_multiple_overrides(tmp_path):
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles",
            "coder_app",
            "--groups",
            "group-a",
            "--override",
            "coder_app:cpu_limit=6",
            "--override",
            "coder_app:mem_limit=12G",
            "--override",
            "coder_app:image=ghcr.io/terradue/coder:latest",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output

    config = read_yaml(output)
    profile = config["profiles"][0]
    kube_override = profile["definition"]["kubespawner_override"]
    assert kube_override["cpu_limit"] == 6
    assert kube_override["mem_limit"] == "12G"
    assert kube_override["image"] == "ghcr.io/terradue/coder:latest"