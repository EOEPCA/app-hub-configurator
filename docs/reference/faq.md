# FAQ

## Why are profiles Python classes?

Profiles contain logic (volumes, config maps, manifests, defaults). Python provides:

- reuse via inheritance
- composition helpers
- clear versioning in Git

## Can I override everything?

Only fields supported by CLI override parsing.

If you need more fields, extend:

- `apply_overrides()`
- documentation and tests

## How do I add my own profiles?

Use:

```bash
dump-config --profiles-dir ./my-profiles --list-profiles
```