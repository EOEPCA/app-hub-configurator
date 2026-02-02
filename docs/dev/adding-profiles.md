## Create a new profile class

Example:

```python
from configurator.apps import profile_registry
from configurator.apps.coder.base_coder import BaseCoderProfile

class MyProfile(BaseCoderProfile):
    slug = "my_profile"
    display_name = "My Profile"
    description = "Example profile"

profile_registry.register(MyProfile)
```

## Config maps

Config maps are stored in:

`apps/<family>/config_maps/<slug>/`

Example:

`apps/coder/config_maps/coder_app/`

## Manifests

Manifests are stored in:

`apps/<family>/manifests/<slug>/`

Use `load_manifests()` helper to load YAML documents into structured objects.