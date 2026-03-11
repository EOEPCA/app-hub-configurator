# Manifests

Profiles can attach Kubernetes manifests to the generated YAML through the `manifests` field.

In this project, manifests are stored as structured YAML documents, not as raw strings.

## Why structured manifests matter

Raw YAML strings are hard to read and hard to post-process:

```yaml
content: "---\napiVersion: ..."
```

Structured output is the intended representation:

```yaml
content:
  - apiVersion: v1
    kind: ServiceAccount
```

This is also what the test suite validates.

## Loading manifests

Use `configurator.apps.app_helpers.load_manifests()`:

```python
from configurator.apps.app_helpers import load_manifests


def get_manifests(self):
    return [
        load_manifests(
            name="local-stack-coder-app",
            key="local-stack",
            file_path="/path/to/manifest.yaml",
            slug=self.slug,
        )
    ]
```

Current helper signature:

```python
def load_manifests(*, name: str, key: str, file_path: str, slug: str) -> Manifest:
    ...
```

Behavior:

- reads one file containing one or more YAML documents
- parses documents with `yaml.safe_load_all`
- drops empty documents produced by `---`
- returns a `Manifest` Pydantic object with `persist=False`

## Template placeholders

Manifest files may contain template placeholders that are intended for later rendering by the consumer side, for example:

- `{{ namespace }}`
- `{{ spawner.user.name }}`

Configurator preserves these values when loading and writing the YAML.

## Recommended layout

Keep manifest files close to the profile family that owns them, for example:

- `configurator/apps/coder/manifests/...`
- `configurator/apps/remote_desktop/manifests/...`

The loader is path-based, so the exact folder name is a project convention, not a hard requirement.

## Testing manifests

If a profile emits manifests, add tests that verify:

- manifests are present in the generated config
- `content` is structured YAML data, not a string
- each document includes expected Kubernetes keys such as `apiVersion` and `kind`

Relevant tests:

- `tests/test_cli_manifests_dumping.py`
