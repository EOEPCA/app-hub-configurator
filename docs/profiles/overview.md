# Profiles overview

Profiles are Python classes registered in the `ProfileRegistry`.

Each profile provides:

- `slug` (unique key)
- `display_name`
- `description`
- container image
- default CPU/memory
- volumes
- config maps
- init containers
- manifests
- role bindings
- node selector
- pod environment variables

## Built-in profile families

- Coder (code-server)
- Remote desktop (noVNC-based)

See:

- Coder profiles
- Remote desktop profiles