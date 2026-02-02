# External profiles (plugins)

Configurator supports loading profiles from external folders using `--profiles-dir`.

This enables:

- custom deployments
- site-specific profiles
- local experiments
- profiles maintained outside the main repository


## Folder structure

Example plugin folder:

```
my-profiles/
├── my_coder_profiles.py
└── init.py
```

`my_coder_profiles.py` must import and register profiles into `profile_registry`.

## Example plugin module

```python
from configurator.apps import profile_registry
from configurator.apps.coder.base_coder import BaseCoderProfile

class MyCustomCoder(BaseCoderProfile):
    slug = "my_custom_coder"
    display_name = "My Custom Coder"
    description = "Custom coder profile"

profile_registry.register(MyCustomCoder)
```

## Load plugins

```bash
dump-config \
  --profiles-dir ./my-profiles \
  --profiles my_custom_coder \
  --groups group-a \
  --output config.yaml
```