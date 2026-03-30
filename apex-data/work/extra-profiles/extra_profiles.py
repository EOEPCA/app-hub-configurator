import os
from configurator.apps import profile_registry
from configurator.apps.coder.base_coder import BaseCoderProfile
from configurator.apps.jupyterlab.base_jupyterlab import BaseJupyterLabProfile
from configurator.apps.remote_desktop.base_remote_desktop import BaseRemoteDesktopProfile
from loguru import logger
class MlflowCoderProfile(BaseCoderProfile):
    slug = "mlflow_coder_app"
    display_name = "Coder + MLflow"
    description = "Code Server with MLflow deployed"

    workspace_volume_size = "15Gi"
    calrissian_volume_size = "30Gi"

    storage_class_rwo = "standard"
    storage_class_rwx = "standard"

    def get_manifests(self):
        # you can reuse your existing load_manifests helper
        from configurator.apps.app_helpers import load_manifests
        import os

        base_path = os.path.dirname(__file__)
        manifest_path = os.path.join(base_path, "manifests/mlflow.yaml")

        return [
            load_manifests(
                name="mlflow",
                key="mlflow",
                file_path=manifest_path,
                slug=self.slug,
            )
        ]

class APEXJupyterLabProfile(BaseJupyterLabProfile):
    slug = "apex_jupyter_lab_app"
    display_name = "Jupyter Lab"
    description = "Interactive development environment for notebooks, code, and data"

    workspace_volume_size = "20Gi"
    calrissian_volume_size = "20Gi"

    storage_class_rwo = "standard"
    storage_class_rwx = "standard"
    base_path = os.path.dirname(__file__)
    bashrc_path = os.path.join(base_path, f"config-maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config-maps/{slug}/init.sh")
    
    if os.path.exists(init_script_path):
        logger.info(f"Init script path {slug} exists!")
    else:
        logger.error(f"Init script path {slug} does not exist!")
        import sys
        sys.exit(1)
    pod_env_vars={
        "HOME": "/workspace",
        "CONDA_ENVS_PATH": "/workspace/.envs",
        "CONDARC": "/workspace/.condarc",
        "XDG_RUNTIME_DIR": "/workspace/.podman",
        "XDG_CONFIG_HOME": "/workspace/.podman",
        "XDG_DATA_HOME": "/workspace/.podman/share/",
        "CWLTOOL_OPTIONS": "--podman",
        "NOTEBOOK_ARGS": "--notebook-dir=/workspace",
        "JUPYTER_PATH": "/workspace/.jupyter",
        "NAMESPACE": "{{ namespace }}",
        }
    def get_manifests(self):
        # you can reuse your existing load_manifests helper
        from configurator.apps.app_helpers import load_manifests
        import os
        
        base_path = os.path.dirname(__file__)
        manifest_path = os.path.join(base_path, f"manifests/{self.slug}/local-stack.yaml")
        if os.path.exists(manifest_path):
            logger.info(f"Manifest path {self.slug} exists: {manifest_path}")
        else:
            logger.error(f"Manifest path {self.slug} does not exist!")
            import sys
            sys.exit(1)
        return [
            load_manifests(
                name="jupyter_lab",
                key="jupyter_lab",
                file_path=manifest_path,
                slug=self.slug,
            )
        ]
class APEXCoderProfile(BaseCoderProfile):
    slug = "apex_coder_app"
    display_name = "Code Server"
    description = "Develop Application Packages at scale"

    workspace_volume_size = "20Gi"
    calrissian_volume_size = "20Gi"

    storage_class_rwo = "standard"
    storage_class_rwx = "standard"

    base_path = os.path.dirname(__file__)
    bashrc_path = os.path.join(base_path, f"config-maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config-maps/{slug}/init.sh")
    if os.path.exists(init_script_path):
        logger.info(f"Init script path {slug} exists!")
    else:
        logger.error(f"Init script path {slug} does not exist!")
        import sys
        sys.exit(1)
    pod_env_vars={
        "HOME": "/workspace",
        "CONDA_ENVS_PATH": "/workspace/.envs",
        "CONDARC": "/workspace/.condarc",
        "XDG_RUNTIME_DIR": "/workspace/.podman",
        "XDG_CONFIG_HOME": "/workspace/.podman",
        "XDG_DATA_HOME": "/workspace/.podman/share/",
        "CWLTOOL_OPTIONS": "--podman",
        "NAMESPACE": "{{ namespace }}",
        }
    def get_manifests(self):
        # you can reuse your existing load_manifests helper
        from configurator.apps.app_helpers import load_manifests
        import os
        
        base_path = os.path.dirname(__file__)
        manifest_path = os.path.join(base_path, f"manifests/{self.slug}/local-stack.yaml")
        if os.path.exists(manifest_path):
            logger.info(f"Manifest path {self.slug} exists: {manifest_path}")
        else:
            logger.error(f"Manifest path {self.slug} does not exist!")
            import sys
            sys.exit(1)
        return [
            load_manifests(
                name="coder",
                key="coder",
                file_path=manifest_path,
                slug=self.slug,
            )
        ]
class APEXRemoteQgisDesktopProfile(BaseRemoteDesktopProfile):
    slug = "apex_remote_qgis_desktop_app"
    display_name = "QGIS on a Remote Desktop"
    description = "Spatial visualization and decision-making tools for everyone"
    image = "ghcr.io/eoepca/iga-remote-desktop-qgis:latest-dev"
    

    storage_class_rwo = "standard"
    storage_class_rwx = "standard"

    base_path = os.path.dirname(__file__)
    bashrc_path = os.path.join(base_path, f"config-maps/{slug}/bash-rc")
    if os.path.exists(bashrc_path):
        print(f"Bashrc path {slug} exists under {base_path}!")
    else:
        print(f"Bashrc path {slug} does not exist under {base_path}!")
        import sys
        sys.exit(1)
    bash_login_path = os.path.join(base_path, f"config-maps/{slug}/bash-login")
    if os.path.exists(bash_login_path):
        print(f"Bash login path {slug} exists!")
    else:
        print(f"Bash login path {slug} does not exist!")
        import sys
        sys.exit(1)
    init_script_path = os.path.join(base_path, f"config-maps/{slug}/init.sh")
    if os.path.exists(init_script_path):
        print(f"Init script path {slug} exists!")
    else:
        print(f"Init script path {slug} does not exist!")
        import sys
        sys.exit(1)
    
profile_registry.register(MlflowCoderProfile)
profile_registry.register(APEXJupyterLabProfile)
profile_registry.register(APEXCoderProfile)
profile_registry.register(APEXRemoteQgisDesktopProfile)