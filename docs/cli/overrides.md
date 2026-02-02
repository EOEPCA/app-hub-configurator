# Overrides

Overrides let operators adjust profile parameters without modifying profile code.

## Field overrides

Use:

```bash
--override <slug>:<field>=<value>
```

Example:

```bash
dump-config \
  --profiles coder_app \
  --groups group-a \
  --override coder_app:cpu_limit=4 \
  --override coder_app:mem_limit=8G
```

## Supported fields

The CLI supports overriding:

* cpu_limit
* cpu_guarantee
* mem_limit
* mem_guarantee
* image
* groups

Example:

```bash
dump-config \
  --profiles coder_app \
  --groups group-a \
  --override coder_app:image=ghcr.io/terradue/coder:latest
```

## Type handling

* `cpu_limit` and `cpu_guarantee` must be integers
* `groups` must be comma-separated list

Invalid CPU values fail fast:

```bash
dump-config \
  --profiles coder_app \
  --groups group-a \
  --override coder_app:cpu_limit=not_an_int
```

## Node selector overrides

Node selectors are overridden with:

```bash
--node-selector <slug>:<key>=<value>
```

Example:

```bash
dump-config \
  --profiles gpu_coder_app \
  --groups group-a \
  --node-selector gpu_coder_app:nodepool=gpu
```

Note: this merges with profile defaults (it does not replace them).


