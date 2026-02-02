# CLI overview

The CLI entrypoint is:

```bash
dump-config
```

It generates an Application Hub YAML configuration.

## Help

```bash
dump-config --help
```

## Main options

```bash
Usage: dump-config [OPTIONS]

  Generate an application-hub configuration YAML.

Options:
  --profiles TEXT           Comma-separated list of enabled profile slugs
                            [default: coder_app]
  --groups TEXT             Comma-separated list of groups  [default:
                            developers]
  --output TEXT             Output YAML file  [default: config.yaml]
  --storage-class-rwo TEXT  StorageClass for ReadWriteOnce volumes
  --storage-class-rwx TEXT  StorageClass for ReadWriteMany volumes
  --node-selector TEXT      Override node selector for a profile. Format:
                            <slug>:<key>=<value>. Can be repeated.
  --override TEXT           Override profile attributes. Format:
                            <slug>:<field>=<value>. Can be repeated.
  --list-profiles           List available registered profile slugs and exit
  --describe-profile SLUG   Print a human-readable summary of a profile and
                            exit
  --profiles-dir DIRECTORY  Extra folder(s) containing python modules/packages
                            defining additional profiles. Modules must
                            register into profile_registry.
  --help                    Show this message and exit.
```


## Profile loading order

* Built-in profiles are registered
* External profile folders are loaded (if any)
* CLI resolves enabled slugs and builds config