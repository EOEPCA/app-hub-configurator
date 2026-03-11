# Adding Profiles

Profiles are regular Python classes that inherit from a base profile family and register themselves into `profile_registry`.

## 1. Pick the right family

Use an existing family when the runtime behavior already matches your app:

- `BaseCoderProfile`
- `BaseRemoteDesktopProfile`
- `BaseJupyterLabProfile`

Only create a new family if you need a new set of shared defaults or hooks.

## 2. Add the profile class

Example:

```python
from configurator.apps import profile_registry
from configurator.apps.coder.base_coder import BaseCoderProfile


class MyProfile(BaseCoderProfile):
    slug = "my_profile"
    display_name = "My Profile"
    description = "Example profile"
    image = "ghcr.io/example/my-profile:latest"


profile_registry.register(MyProfile)
```

Required class attributes:

- `slug`
- `display_name`
- `description`
- `image`

Common optional attributes:

- `cpu_guarantee`, `cpu_limit`
- `mem_guarantee`, `mem_limit`
- `default_url`
- `bash_login_path`
- `bashrc_path`
- `init_script_path`

## 3. Place the profile in the correct package

Built-in profiles live under `configurator/apps/<family>/`.

Typical pattern:

- add the class to `coder_profiles.py`, `remote_desktop_profiles.py`, or `jupyterlab_profiles.py`
- export it from the package `__init__.py`
- register it in that same `__init__.py`

Example registration in `configurator/apps/coder/__init__.py`:

```python
from configurator.apps import profile_registry
from .coder_profiles import CoderProfile, GpuCoderProfile

profile_registry.register(CoderProfile)
profile_registry.register(GpuCoderProfile)
```

## 4. Add supporting files if needed

The codebase uses file-backed assets for shell setup and manifests.

Common locations:

- `configurator/apps/<family>/config_maps/...`
- `configurator/apps/<family>/manifests/...`

Profiles reference these assets through explicit paths in Python, for example:

```python
import os

base_path = os.path.dirname(__file__)
bashrc_path = os.path.join(base_path, "config_maps/my_profile/bash-rc")
init_script_path = os.path.join(base_path, "config_maps/my_profile/init.sh")
```

There is no automatic convention-based loading. If you add a file, you must wire it in from Python.

## 5. Override hooks only when needed

Most profiles should override a small subset of hooks:

- `get_default_volumes()` for additional storage
- `get_manifests()` for structured Kubernetes resources
- `get_config_maps()` for extra mounted files
- `get_pod_env_vars()` for environment variables
- `get_extra_resource_limits()` for GPU or other extended resources

Do not override `build()` unless you are changing the output contract itself.

## 6. Add tests

At minimum, add or extend tests for:

- successful CLI generation with the new slug
- any profile-specific overrides
- manifests if the profile emits them
- plugin loading if the profile is meant to be external

Useful test files to mirror:

- `tests/test_cli_dump_config.py`
- `tests/test_cli_overrides.py`
- `tests/test_cli_manifests_dumping.py`
- `tests/test_external_profiles.py`

## External profiles

For site-specific or experimental profiles, prefer external plugin modules loaded with `--profiles-dir`.

Behavior today:

- every top-level Python module/package inside the provided folder is imported
- imported modules are expected to register into `profile_registry`
- duplicate slugs fail fast

Minimal external profile example:

```python
from configurator.apps import profile_registry
from configurator.apps.base import BaseAppProfile


class ExternalProfile(BaseAppProfile):
    slug = "external_profile"
    display_name = "External Profile"
    description = "Loaded from --profiles-dir"
    image = "alpine:3.19"


profile_registry.register(ExternalProfile)
```
