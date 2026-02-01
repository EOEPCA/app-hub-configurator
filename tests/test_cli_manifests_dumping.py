from click.testing import CliRunner

from configurator.main import main
from tests.helpers import read_yaml, get_slugs, assert_manifest_content_is_structured


def test_manifests_dumped_as_structured_yaml(tmp_path):
    """
    Ensure manifests.content is YAML structured data, not a YAML string.
    """
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles",
            "coder_dask_gateway_app",
            "--groups",
            "group-a",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output
    assert output.exists()

    config = read_yaml(output)
    assert get_slugs(config) == ["coder_dask_gateway_app"]

    profile = config["profiles"][0]

    # must have manifests
    assert "manifests" in profile
    assert len(profile["manifests"]) >= 1

    assert_manifest_content_is_structured(profile)


def test_manifests_are_not_serialized_as_yaml_string(tmp_path):
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles",
            "coder_dask_gateway_app",
            "--groups",
            "group-a",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output

    raw = output.read_text()

    # manifests should NOT contain a giant YAML string with embedded document separators
    assert 'manifests:\n  - content: "---\\n' not in raw
    assert "manifests:\n  - content: '---\\n" not in raw


def test_manifest_docs_have_kind_and_metadata(tmp_path):
    runner = CliRunner()
    output = tmp_path / "config.yaml"

    result = runner.invoke(
        main,
        [
            "--profiles",
            "coder_dask_gateway_app",
            "--groups",
            "group-a",
            "--output",
            str(output),
        ],
    )
    assert result.exit_code == 0, result.output

    config = read_yaml(output)
    profile = config["profiles"][0]

    manifests = profile["manifests"]
    docs = manifests[0]["content"]

    for doc in docs:
        assert "kind" in doc
        assert "apiVersion" in doc
        # metadata is optional for some objects, but usually present
        if doc["kind"] not in {"List"}:
            assert "metadata" in doc
