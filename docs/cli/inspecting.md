# Inspecting profiles

## List all registered profiles

```bash
dump-config --list-profiles
```

## Describe a profile

```bash
dump-config --describe-profile coder_dask_gateway_app
```

This prints:

* display name
* description
* image
* CPU/memory defaults
* volumes
* env vars
* manifests summary
* supported override fields