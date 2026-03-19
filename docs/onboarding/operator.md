# Operator onboarding

This guide is for platform operators generating Application Hub configuration.

## 1. Install and verify

Use one of:

```bash
pip install app-hub-configurator
dump-config --help
```

or from source:

```bash
hatch run dump-config --help
```

## 2. Generate your first config

```bash
dump-config \
  --profiles coder_app,gpu_coder_app \
  --groups group-a,group-b \
  --output config.yaml
```

## 3. Inspect what is available

```bash
dump-config --list-profiles
dump-config --describe-profile coder_app
```

## 4. Apply runtime overrides

```bash
dump-config \
  --profiles coder_app \
  --groups group-a \
  --override coder_app:cpu_limit=4 \
  --override coder_app:mem_limit=8G \
  --output config.yaml
```

## 5. Use external profile plugins

```bash
dump-config \
  --profiles-dir ./my-profiles \
  --profiles my_custom_profile \
  --groups group-a \
  --output config.yaml
```

## 6. Recommended first reads

- `docs/getting-started.md`
- `docs/cli/overview.md`
- `docs/cli/plugins.md`
- `docs/cli/troubleshooting.md`

## 7. Skaffold workflow (cluster deployment path)

If you deploy Application Hub through Helm/Skaffold, use the repository `skaffold.yaml`.

Typical flow:

1. Generate `config.yaml` with `dump-config`.
2. Deploy using one of the Skaffold profiles:
   - `baseline`
   - `develop`
   - `main`

Example:

```bash
skaffold run -p develop
```

Notes:

- `skaffold.yaml` injects `config.yaml` into the chart values (`setFiles.configYml`).
- Image/tag selection is profile-based in Skaffold.
