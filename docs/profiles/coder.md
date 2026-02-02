# Coder profiles

Coder profiles are based on `BaseCoderProfile`.

They provide:

- workspace volume (`/workspace`)
- calrissian volume (`/calrissian`)
- bash config maps
- init script
- default CPU/memory values
- optional manifests (e.g. Dask Gateway)

## Examples

- `coder_app`
- `gpu_coder_app`
- `coder_dask_gateway_app`
- `training_how_to_app`

## Dask Gateway profile

`coder_dask_gateway_app` includes structured manifests:

- Helm Release (Crossplane)
- ConfigMaps
- RBAC roles and bindings