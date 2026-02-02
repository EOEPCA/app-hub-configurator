# Manifests

Manifests are loaded from YAML files and stored as **structured YAML objects**, not strings.

## Why structured manifests?

If manifests are stored as raw strings, YAML becomes unreadable:

```yaml
content: "---\napiVersion: ..."
```

Instead, we want:

```yaml
content:
  - apiVersion: v1
    kind: ServiceAccount
```

## Loading manifests

Use helper:

```python
def load_manifests(*, name: str, key: str, file_path: str) -> Manifest:
    with open(file_path, "r") as f:
        content = [literalize_multiline(doc) for doc in yaml.safe_load_all(f)]

    return Manifest(
        name=name,
        key=key,
        persist=False,
        content=content,
    )
```

## Template rendering

The server-side config reader supports Jinja2 rendering selectively after parsing YAML.

This enables manifests to include:

* `{{ namespace }}`
* `{{ spawner.user.name }}`