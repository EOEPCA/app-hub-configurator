# Config schema

The generated YAML follows the Application Hub schema:

```yaml
profiles:
  - id: profile_coder_app
    groups: [...]
    definition:
      slug: coder_app
      display_name: ...
      description: ...
      kubespawner_override:
        cpu_limit: ...
        mem_limit: ...
    volumes: [...]
    config_maps: [...]
    manifests: [...]
    role_bindings: [...]
```

The canonical schema is defined by configurator.models.