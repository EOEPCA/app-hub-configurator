# Configurator

**Configurator** is a CLI that generates an `application-hub` compatible YAML configuration from a set of Python-defined profiles.

It is designed to:

- keep profiles versioned in Git
- support multiple profiles in one output file
- allow operator overrides via CLI options (CPU/memory/image/groups/node selectors)
- support profile plugins loaded from external folders
- preserve multi-line values using YAML literal blocks (`|`) for readability
- support structured manifests (YAML objects), not string blobs

---

## Quick example

Generate a config enabling multiple profiles:

```bash
dump-config \
  --profiles coder_app,gpu_coder_app,remote_desktop,qgis_remote_desktop,coder_dask_gateway_app,training_how_to_app \
  --groups group-a,group-b,group-c \
  --output config.yaml
```

## Concepts

### Profiles

A profile is a Python class registered into the ProfileRegistry with a unique slug.

Profiles define defaults for:

* container image
* CPU/memory limits/guarantees
* volumes
* config maps
* init containers
* manifests
* role bindings
* node selector
* env vars

### Overrides

Operators can override profile defaults without changing code, e.g.:

```
dump-config \
  --profiles coder_app \
  --groups group-a \
  --override coder_app:cpu_limit=4 \
  --override coder_app:mem_limit=8G
```

## Documentation

Start here: Getting started

For users/operators: CLI docs

For developers: Developer guide