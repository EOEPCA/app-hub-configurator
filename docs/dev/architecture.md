# Architecture

Configurator builds an Application Hub YAML file from Python profile classes.

The runtime is organized around five layers:

- registry: stores concrete profile classes by slug
- profile families: provide shared defaults and hooks for a class of apps
- CLI: resolves user input, loads profiles, applies overrides, and writes output
- models: Pydantic schema for the generated configuration
- IO/helpers: YAML serialization plus config map / manifest helpers

## Main modules

- `configurator.main`
  Thin module that exposes the CLI entrypoint by importing `configurator.cli.commands.main`.
- `configurator.cli.commands`
  Defines the `dump-config` Click command and all supported options.
- `configurator.plugins.loader`
  Imports built-in profile packages and optionally imports external plugin modules from `--profiles-dir`.
- `configurator.apps.registry.ProfileRegistry`
  Central in-memory registry keyed by profile slug.
- `configurator.apps.base.BaseAppProfile`
  Base class that assembles a `Profile` Pydantic object.
- `configurator.models`
  Pydantic models for profiles, volumes, role bindings, manifests, config maps, and the final `Config`.
- `configurator.io.yaml_writer`
  Writes the final YAML using `ruamel.yaml`.

## Data flow

1. `dump-config` starts in `configurator.cli.commands.main`.
2. Built-in profiles are registered by importing:
   - `configurator.apps.coder`
   - `configurator.apps.remote_desktop`
   - `configurator.apps.jupyterlab`
3. External profile folders passed through `--profiles-dir` are added to `sys.path`, then every top-level module/package in those folders is imported.
4. CLI arguments are parsed into:
   - enabled profile slugs
   - groups
   - node selector overrides
   - attribute overrides
5. Each selected profile class is looked up in `profile_registry`, instantiated, and optionally overridden.
6. `BaseAppProfile.build()` converts the profile instance into a `configurator.models.Profile`.
7. All built profiles are wrapped in `configurator.models.Config`.
8. `configurator.io.yaml_writer.write_yaml()` serializes the config to disk.

## Registration model

Profiles do not use auto-discovery inside the repository.

Registration happens explicitly at import time in package `__init__.py` files, for example:

```python
from configurator.apps import profile_registry
from .coder_profiles import CoderProfile

profile_registry.register(CoderProfile)
```

This keeps profile availability deterministic and makes test setup straightforward.

## Profile lifecycle

`BaseAppProfile` exposes hooks that subclasses override to contribute data:

- `get_default_volumes()`
- `get_manifests()`
- `get_role_bindings()`
- `get_config_maps()`
- `get_image_pull_secrets()`
- `get_env_config_maps()`
- `get_env_secrets()`
- `get_secret_mounts()`
- `get_pod_env_vars()`
- `get_extra_resource_limits()`

Concrete profiles should define identity and defaults through class attributes such as:

- `slug`
- `display_name`
- `description`
- `image`
- `cpu_guarantee`, `cpu_limit`
- `mem_guarantee`, `mem_limit`
- `default_url`
- optional file-backed paths like `bashrc_path` and `init_script_path`

`build()` is implemented once in `BaseAppProfile` and should normally not be overridden.

## Built-in profile families

- `configurator.apps.coder`
  Registers `coder_app`, `gpu_coder_app`, `coder_dask_gateway_app`, and `training_how_to_app`.
- `configurator.apps.remote_desktop`
  Registers `remote_desktop`, `qgis_remote_desktop`, `panoply_remote_desktop`, and `snap_remote_desktop`.
- `configurator.apps.jupyterlab`
  Registers `jupyterlab_small`.

Each family packages its own defaults, supporting config maps, and manifests alongside the Python classes.

## Overrides

Overrides are handled in two steps:

- `configurator.overrides.parser`
  Parses `--override` and `--node-selector` CLI values.
- `configurator.overrides.apply`
  Validates and applies attribute overrides to instantiated profiles.

Examples:

- `coder_app:cpu_limit=4`
- `gpu_coder_app:image=ghcr.io/example/gpu:latest`
- `gpu_coder_app:nodepool=gpu`

## YAML output

The final config is emitted through `ruamel.yaml`.

Important behavior:

- manifests are written as structured YAML objects, not YAML-encoded strings
- multi-line config map content is preserved as literal blocks where applicable
- output is based on the Pydantic model graph, not ad hoc dict assembly
