# Architecture

Configurator is structured around:

- profile registry
- profile classes
- config models
- CLI entrypoint

## Key modules

- `configurator.apps.registry.ProfileRegistry`
- `configurator.apps.base.BaseAppProfile`
- `configurator.models` (Pydantic models)
- `configurator.main` (Click CLI)

## Data flow

1. CLI loads profiles (built-in + plugins)
2. enabled slugs are resolved from registry
3. profiles are instantiated
4. CLI applies overrides
5. profiles are built into Pydantic `Config`
6. YAML is dumped using ruamel.yaml with multiline literals