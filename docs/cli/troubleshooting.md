# Troubleshooting

## Unknown profile slug

If you see:

`Error: Unknown profile slug '...'`

Run:

```bash
dump-config --list-profiles
```

### Invalid override format

Override format must be:

`<slug>:<field>=<value>`

Example:

```bash
--override coder_app:cpu_limit=4
```

## YAML contains escaped strings

This happens if multi-line values are treated as plain strings.

Configurator uses ruamel.yaml and wraps multi-line values as |.

If you add new models containing multi-line values, ensure they go through:

`literalize_multiline_values()`

## External profiles not loaded

Ensure plugin modules are top-level in the folder:

```bash
dump-config --profiles-dir ./plugins --list-profiles
```

If you don’t see your slug:

* check sys.path importability
* ensure the module registers into `profile_registry`