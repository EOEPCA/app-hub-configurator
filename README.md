# Configurator – Application Hub Profile Generator

`configurator` is a framework and CLI tool to define, compose, and export application profiles (Code Server, GPU Code Server, Remote Desktop, …) into a single YAML configuration consumable by an Application Hub (e.g. JupyterHub + KubeSpawner).

The design focuses on:

- explicit configuration (no magic)
- strong typing (Pydantic)
- extensible base classes
- deterministic profile selection
- deployment-time overrides via CLI

## Core Concepts

### Profile

A `Profile` represents a runnable application configuration:

* container image
* CPU / memory limits
* node selector
* volumes
* environment variables
* config maps
* init containers
* optional default URL

Profiles are serialized into a YAML file via the Config model.

### BaseAppProfile

`BaseAppProfile` is the foundation for all applications.

It implements:

* profile construction (`build()`)
* resource wiring
* config map handling
* init containers
* volume merging
* node selector handling
* default URL propagation

Concrete profiles never override `build()`.

### App Families

Profiles are grouped by base app classes:

* `BaseCoderProfile` → code / notebook / CWL apps
* `BaseRemoteDesktopProfile` → web-based desktop apps
* (future) `BaseJupyterLabProfile`, `BaseDashboardProfile`, …

Each family defines sane defaults for:

* image
* resources
* volumes
* environment

### Profile Registry

Profiles are registered explicitly in a central registry.

* Each profile has a unique slug
* Deployments select profiles by slug
* No auto-discovery or hidden imports

This makes profile selection deterministic and debuggable.

### Repository Structure

```
configurator/
  apps/
    base.py                    # BaseAppProfile
    registry.py                # ProfileRegistry

    coder/
      base_coder.py            # BaseCoderProfile
      coder_profiles.py        # CoderProfile, GpuCoderProfile
      __init__.py              # re-exports + registration

    remote_desktop/
      base_remote_desktop.py   # BaseRemoteDesktopProfile
      remote_desktop_profiles.py
      __init__.py              # re-exports + registration

  models.py                    # Pydantic models
  main.py                      # click-based CLI entrypoint
```

### Defining Profiles

#### Example: Base coder profile

```python
class BaseCoderProfile(BaseAppProfile):
    image = "ghcr.io/terradue/coder:latest"
    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "4G"
    mem_limit = "6G"
```

#### Example: Concrete coder profile

```python
class CoderProfile(BaseCoderProfile):
    display_name = "Code Server"
    description = "Code Server for development"
    slug = "coder_app"
```

#### Example: GPU coder profile

```python
class GpuCoderProfile(BaseCoderProfile):
    display_name = "GPU Code Server"
    description = "Code Server with GPU acceleration"
    slug = "gpu_coder_app"

    cpu_limit = 8
    mem_limit = "32G"

    def get_extra_resource_limits(self):
        return {"nvidia.com/gpu": 1}
```

#### Example: Remote desktop base profile

```python
class BaseRemoteDesktopProfile(BaseAppProfile):
    image = "ghcr.io/terradue/remote-desktop:latest"
    default_url = "/desktop"
```

### Registering Profiles

Profiles are registered explicitly in their package __init__.py:

```python
from configurator.apps import profile_registry
from .coder_profiles import CoderProfile, GpuCoderProfile

profile_registry.register(CoderProfile)
profile_registry.register(GpuCoderProfile)
```

Only **concrete profiles** are registered.

Base classes are never registered.

### CLI: dump-config

The CLI is implemented using `Click`.

```
dump-config --help
```

#### Options

Option	Description
--profiles	Comma-separated list of profile slugs
--groups	Comma-separated list of groups
--image	Default image (overrides base default)
--node-selector	Per-profile node selector override
--override	Per-profile attribute override
--output	Output YAML file

Environment variables can be used as defaults.

#### Selecting Profiles

```
dump-config \
  --profiles coder_app,gpu_coder_app,remote_desktop
```

Profiles are selected by slug, in order.

#### Groups

```
dump-config \
  --profiles coder_app \
  --groups developers,ml-users
```

Groups are deployment-level policy and apply to all selected profiles.

#### Node Selector Overrides (per slug)

Syntax

```
--node-selector <slug>:<key>=<value>
```

Example

```
dump-config \
  --profiles coder_app,gpu_coder_app \
  --node-selector gpu_coder_app:nodepool=gpu
```

Result (excerpt)

```yaml
profiles:
  - id: profile_gpu_coder_app
    node_selector:
      nodepool: gpu
```

### Resource & Image Overrides (per slug)

Syntax

`--override <slug>:<field>=<value>`


Supported fields include:

* `cpu_limit`
* `cpu_guarantee`
* `mem_limit`
* `mem_guarantee`
* `image`
* any other profile attribute

#### Example: CPU & memory

```
dump-config \
  --profiles coder_app \
  --override coder_app:cpu_limit=4 \
  --override coder_app:mem_limit=8G
```

#### Example: image override

```
dump-config \
  --profiles coder_app \
  --override coder_app:image=ghcr.io/terradue/coder:2024.11
```

Combined Example

```
dump-config \
  --profiles coder_app,gpu_coder_app,remote_desktop \
  --groups developers,ml-users \
  --node-selector gpu_coder_app:nodepool=gpu \
  --override coder_app:cpu_limit=4 \
  --override gpu_coder_app:mem_limit=32G \
  --output config.yaml
```

### Output

The CLI generates a single YAML file:

```yaml
profiles:
  - id: profile_coder_app
    groups:
      - developers
      - ml-users
    definition:
      display_name: Code Server
      slug: coder_app
      kubespawner_override:
        cpu_limit: 4
        mem_limit: 6G
        image: ghcr.io/terradue/coder:latest
```

Serialization uses:

`config.model_dump(exclude_none=True)`


No Python-specific YAML tags are emitted.

## Design Rules (Important)

* Profiles define defaults, not deployment policy
* Deployment overrides happen only via the CLI
* Selection is by slug, not by class name
* Concrete profiles never override build()
* Base classes define shared behavior
* CLI remains the single control plane

## Why This Architecture Scales

This design supports, without refactoring:

* new app families
* cluster-specific overrides
* GPU / non-GPU deployments
* multiple environments
* CI-generated configs
* Helm / GitOps workflows

## License

