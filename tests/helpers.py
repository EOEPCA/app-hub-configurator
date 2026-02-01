import yaml


def read_yaml(path):
    return yaml.safe_load(path.read_text())


def get_slugs(config):
    return [p["definition"]["slug"] for p in config["profiles"]]


def assert_manifest_content_is_structured(profile: dict):
    """
    Assert manifests are represented as list[dict], not YAML-as-a-string.
    """
    manifests = profile.get("manifests", [])
    assert isinstance(manifests, list)

    for m in manifests:
        assert "content" in m, f"manifest missing content: {m}"
        content = m["content"]

        # Must NOT be a string containing YAML text
        assert not isinstance(content, str), (
            f"manifest content is string: {content[:100]}"
        )

        # Must be a list of YAML docs
        assert isinstance(content, list), (
            f"manifest content should be list, got {type(content)}"
        )

        # Each doc must be a mapping
        for doc in content:
            assert isinstance(doc, dict), (
                f"manifest doc should be dict, got {type(doc)}"
            )
            assert "apiVersion" in doc
            assert "kind" in doc
