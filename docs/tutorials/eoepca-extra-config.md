# Tutorial: EOEPCA extra config with plugin profiles

This tutorial shows how to generate a `config.yaml` that enables these applications in Application Hub:

| Application | Repository |
|-------------|------------|
| Processor Development Environment | [EOEPCA/pde-code-server](https://github.com/EOEPCA/pde-code-server) |
| JupyterLab | [EOEPCA/iat-jupyterlab](https://github.com/EOEPCA/iat-jupyterlab) |
| Remote Desktop | [EOEPCA/iga-remote-desktop](https://github.com/EOEPCA/iga-remote-desktop) |
| Remote Desktop with QGIS | [EOEPCA/iga-remote-desktop-qgis](https://github.com/EOEPCA/iga-remote-desktop-qgis) |
| Remote Desktop with SNAP | [EOEPCA/iga-remote-desktop-snap](https://github.com/EOEPCA/iga-remote-desktop-snap) |
| Remote Desktop with Panoply | [EOEPCA/iga-remote-desktop-panoply](https://github.com/EOEPCA/iga-remote-desktop-panoply) |
| Dashboard with Streamlit | [EOEPCA/iga-streamlit-demo](https://github.com/EOEPCA/iga-streamlit-demo) |

## 1. Prepare plugin folders

This repository already includes EOEPCA coder-related extra profiles in:

- `data/work/extra-profiles`

Create an additional plugin module for Streamlit:

```bash
mkdir -p data/work/tutorial-profiles
cat > data/work/tutorial-profiles/streamlit_profile.py <<'PY'
from configurator.apps import profile_registry
from configurator.apps.base import BaseAppProfile


class StreamlitDashboardProfile(BaseAppProfile):
    slug = "streamlit_dashboard"
    display_name = "Dashboard with Streamlit"
    description = "Interactive Streamlit dashboard"
    image = "ghcr.io/eoepca/iga-streamlit-demo:latest"
    default_url = "/proxy/8501/"

    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "2G"
    mem_limit = "4G"


profile_registry.register(StreamlitDashboardProfile)
PY
```

## 2. Generate `config.yaml`

Run:

```bash
dump-config \
  --profiles-dir data/work/extra-profiles \
  --profiles-dir data/work/tutorial-profiles \
  --profiles eoepca_coder_app,jupyterlab_small,remote_desktop,qgis_remote_desktop,snap_remote_desktop,panoply_remote_desktop,streamlit_dashboard \
  --groups group-a,group-b \
  --output config.yaml
```

## 3. Validate the generated profiles

```bash
yq '.profiles[].definition.slug' config.yaml
```

Expected slugs include:

- `eoepca_coder_app`
- `jupyterlab_small`
- `remote_desktop`
- `qgis_remote_desktop`
- `snap_remote_desktop`
- `panoply_remote_desktop`
- `streamlit_dashboard`

## 4. Deploy with Skaffold

If you deploy via the repository Helm/Skaffold flow:

```bash
skaffold run -p develop
```

`skaffold.yaml` injects `config.yaml` into the chart (`setFiles.configYml` in profile patches).

## 5. Troubleshooting

- Unknown slug errors:
  Ensure both `--profiles-dir` folders are passed and the module file names are unique.
- Streamlit app route:
  If your image uses a different port/path, adjust `default_url` accordingly.
- Profile discovery:
  Use `dump-config --profiles-dir <dir> --list-profiles` to confirm registration.

