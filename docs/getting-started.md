# Getting started

This guide explains how to install and run the `dump-config` CLI.

## Install

From the project root:

```bash
hatch env create
hatch run dump-config --help
```

Or install editable:

```bash
pip install -e .
dump-config --help
```

## Generate a configuration

```bash
dump-config \
  --profiles coder_app,gpu_coder_app \
  --groups group-a,group-b \
  --output config.yaml
```

## Validate output

Inspect the generated YAML:

```bash
yq '.profiles[].definition.slug' config.yaml
```

## List available profiles

```bash
dump-config --list-profiles
```

## Inspect a profile

```bash
dump-config --describe-profile coder_app
```

## Common environment variables

All CLI options support envvars:

* `ENABLED_PROFILES`
* `GROUPS`
* `OUTPUT_FILE`
* `STORAGE_CLASS_RWO`
* `STORAGE_CLASS_RWX`

Example:

``bash
export ENABLED_PROFILES="coder_app,gpu_coder_app"
export GROUPS="group-a,group-b"
dump-config
```