import os
from configurator.models import (
    Volume,
    VolumeMount,
)
from configurator.apps.base import BaseAppProfile


class BaseJupyterLabProfile(BaseAppProfile):
    home_dir = "/workspace"

    image = "ghcr.io/eoepca/iat-jupyterlab:latest-dev"

    base_path = os.path.dirname(__file__)

    bash_login_path = os.path.join(base_path, "config_maps/common/bash-login")

    storage_class_rwo = "standard"

    def get_default_volumes(self) -> list[Volume]:
        return [
            Volume(
                name="workspace-volume",
                size=self.workspace_volume_size,
                claim_name="workspace-claim",
                mount_path="/workspace",
                storage_class=self.storage_class_rwo,
                access_modes=["ReadWriteOnce"],
                volume_mount=VolumeMount(
                    name="workspace-volume", mount_path="/workspace"
                ),
                persist=True,
            ),
        ]

    pod_env_vars = {
        "HOME": home_dir,
        "XDG_RUNTIME_DIR": f"{home_dir}/.local",
        "XDG_CONFIG_HOME": f"{home_dir}/.local",
        "XDG_DATA_HOME": f"{home_dir}/.local/share/",
        "CWLTOOL_OPTIONS": "--podman",
        "NAMESPACE": "{{ namespace }}",
    }

    def get_manifests(self):
        return []

    # coder defaults
    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "4G"
    mem_limit = "6G"
