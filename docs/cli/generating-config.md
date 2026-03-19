# Generating config

## Basic generation

```bash
dump-config \
  --profiles coder_app,remote_desktop \
  --groups group-a,group-b \
  --output config.yaml
```

## Storage classes

Override storage class values:

```bash
dump-config \
  --profiles coder_app \
  --groups group-a \
  --storage-class-rwo standard \
  --storage-class-rwx standard-rwx \
  --output config.yaml
```

## Large profile set

```bash
dump-config \
  --profiles coder_app,gpu_coder_app,remote_desktop,qgis_remote_desktop,panoply_remote_desktop,snap_remote_desktop,coder_dask_gateway_app,jupyterlab_small \
  --groups group-a,group-b,group-c \
  --output config.yaml
```

## YAML formatting

Configurator preserves multi-line values (scripts/configs) using literal blocks:

```yaml
content: |
  echo "Initializing environment..."
  export HOME=/workspace
```

This improves readability and prevents YAML escaping issues.
