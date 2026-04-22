# Tutorial: EOEPCA extra config with all profiles in `extra-profiles`

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

## 1. Create one external profile pack

Create a folder that contains all EOEPCA app profiles as plugin profiles:

```bash
mkdir -p data/work/eoepca-extra-profiles
cat > data/work/eoepca-extra-profiles/eoepca_profiles.py <<'PY'
from configurator.apps import profile_registry
from configurator.apps.base import BaseAppProfile
from configurator.apps.coder.base_coder import BaseCoderProfile
from configurator.apps.jupyterlab.base_jupyterlab import BaseJupyterLabProfile
from configurator.apps.remote_desktop.base_remote_desktop import BaseRemoteDesktopProfile


class EoepcaPdeProfile(BaseCoderProfile):
    slug = "eoepca_pde_app"
    display_name = "Processor Development Environment"
    description = "PDE Code Server"
    image = "ghcr.io/eoepca/pde-code-server:latest-dev"
    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "4G"
    mem_limit = "6G"
    storage_class_rwo = "standard"
    storage_class_rwx = "standard"


class EoepcaJupyterLabProfile(BaseJupyterLabProfile):
    slug = "eoepca_jupyterlab_app"
    display_name = "JupyterLab"
    description = "EOEPCA JupyterLab environment"
    image = "ghcr.io/eoepca/iat-jupyterlab:latest-dev"
    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "4G"
    mem_limit = "6G"
    storage_class_rwo = "standard"


class EoepcaRemoteDesktopProfile(BaseRemoteDesktopProfile):
    slug = "eoepca_remote_desktop"
    display_name = "Remote Desktop"
    description = "EOEPCA Remote Desktop"
    image = "ghcr.io/eoepca/iga-remote-desktop:1.2.0"
    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "4G"
    mem_limit = "6G"
    storage_class_rwo = "standard"


class EoepcaQgisRemoteDesktopProfile(BaseRemoteDesktopProfile):
    slug = "eoepca_qgis_remote_desktop"
    display_name = "Remote Desktop with QGIS"
    description = "EOEPCA Remote Desktop with QGIS"
    image = "ghcr.io/eoepca/iga-remote-desktop-qgis:latest"
    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "4G"
    mem_limit = "6G"
    storage_class_rwo = "standard"


class EoepcaSnapRemoteDesktopProfile(BaseRemoteDesktopProfile):
    slug = "eoepca_snap_remote_desktop"
    display_name = "Remote Desktop with SNAP"
    description = "EOEPCA Remote Desktop with SNAP"
    image = "ghcr.io/eoepca/iga-remote-desktop-snap:latest-dev"
    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "4G"
    mem_limit = "6G"
    storage_class_rwo = "standard"


class EoepcaPanoplyRemoteDesktopProfile(BaseRemoteDesktopProfile):
    slug = "eoepca_panoply_remote_desktop"
    display_name = "Remote Desktop with Panoply"
    description = "EOEPCA Remote Desktop with Panoply"
    image = "ghcr.io/eoepca/iga-remote-desktop-panoply:latest-dev"
    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "4G"
    mem_limit = "6G"
    storage_class_rwo = "standard"


class EoepcaStreamlitDashboardProfile(BaseAppProfile):
    slug = "eoepca_streamlit_dashboard"
    display_name = "Dashboard with Streamlit"
    description = "Interactive Streamlit dashboard"
    image = "ghcr.io/eoepca/iga-streamlit-demo:latest"
    default_url = "/proxy/8501/"

    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "2G"
    mem_limit = "4G"


profile_registry.register(EoepcaPdeProfile)
profile_registry.register(EoepcaJupyterLabProfile)
profile_registry.register(EoepcaRemoteDesktopProfile)
profile_registry.register(EoepcaQgisRemoteDesktopProfile)
profile_registry.register(EoepcaSnapRemoteDesktopProfile)
profile_registry.register(EoepcaPanoplyRemoteDesktopProfile)
profile_registry.register(EoepcaStreamlitDashboardProfile)
PY
```

## 2. Generate `config.yaml` (with storage classes)

Run:

```bash
dump-config \
  --profiles-dir data/work/eoepca-extra-profiles \
  --profiles eoepca_pde_app,eoepca_jupyterlab_app,eoepca_remote_desktop,eoepca_qgis_remote_desktop,eoepca_snap_remote_desktop,eoepca_panoply_remote_desktop,eoepca_streamlit_dashboard \
  --storage-class-rwo managed-nfs-storage \
  --storage-class-rwx cephfs \
  --groups group-a,group-b \
  --output config.yaml
```

## 3. Optional: tune resources per profile

Use `--override` for per-profile CPU and memory:

```bash
dump-config \
  --profiles-dir data/work/eoepca-extra-profiles \
  --profiles eoepca_pde_app,eoepca_jupyterlab_app,eoepca_remote_desktop,eoepca_qgis_remote_desktop,eoepca_snap_remote_desktop,eoepca_panoply_remote_desktop,eoepca_streamlit_dashboard \
  --storage-class-rwo managed-nfs-storage \
  --storage-class-rwx cephfs \
  --groups group-a,group-b \
  --override eoepca_pde_app:cpu_limit=4 \
  --override eoepca_pde_app:mem_limit=8G \
  --override eoepca_jupyterlab_app:cpu_limit=4 \
  --override eoepca_jupyterlab_app:mem_limit=8G \
  --override eoepca_streamlit_dashboard:cpu_limit=2 \
  --override eoepca_streamlit_dashboard:mem_limit=4G \
  --output config.yaml
```

## 4. Validate the generated profiles

```bash
yq '.profiles[].definition.slug' config.yaml
```

Expected slugs include:

- `eoepca_pde_app`
- `eoepca_jupyterlab_app`
- `eoepca_remote_desktop`
- `eoepca_qgis_remote_desktop`
- `eoepca_snap_remote_desktop`
- `eoepca_panoply_remote_desktop`
- `eoepca_streamlit_dashboard`

## 5. Validate resources and storage classes

Inspect resource limits:

```bash
yq '.profiles[].definition.kubespawner_override | {image, cpu_limit, mem_limit}' config.yaml
```

Inspect volume storage classes:

```bash
yq '.profiles[].volumes[].storage_class' config.yaml | sort -u
```

## 6. Deploy with Skaffold

If you deploy via the repository Helm/Skaffold flow:

```bash
skaffold run -p develop
```

`skaffold.yaml` injects `config.yaml` into the chart (`setFiles.configYml` in profile patches).

## 7. Troubleshooting

- Unknown slug errors:
  Ensure `--profiles-dir data/work/eoepca-extra-profiles` is passed.
- Streamlit app route:
  If your image uses a different port/path, adjust `default_url` accordingly.
- Profile discovery:
  Use `dump-config --profiles-dir <dir> --list-profiles` to confirm registration.
- Duplicate slug errors:
  Keep custom slugs unique and avoid reusing built-in slugs such as `coder_app` or `jupyterlab_small`.
- Resource override validation errors:
  Ensure CPU values are integers and memory values are valid strings (example: `8G`).
