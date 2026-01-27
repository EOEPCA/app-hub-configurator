import os
from configurator.apps.base import BaseAppProfile
from configurator.models import Volume, VolumeMount


class BaseRemoteDesktopProfile(BaseAppProfile):
    home_dir = "/workspace"

    # Desktop apps do NOT start at /lab
    default_url = "/desktop"

    image = "ghcr.io/eoepca/iga-remote-desktop:1.2.0"

    storage_class_rwo = "standard"
    storage_class_rwx = "standard"

    pod_env_vars = {
        "HOME": home_dir,
        "CONDA_ENVS_PATH": f"{home_dir}/.envs",
        "CONDARC": f"{home_dir}/.condarc",
        "XDG_RUNTIME_DIR": f"{home_dir}/.local",
        "XDG_CONFIG_HOME": f"{home_dir}/.local",
        "XDG_DATA_HOME": f"{home_dir}/.local/share/",
        "CWLTOOL_OPTIONS": "--podman",
    }

    # defaults
    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "4G"
    mem_limit = "6G"

    # shared config
    base_path = os.path.dirname(__file__)
    bash_login_path = os.path.join(base_path, "config_maps/bash-login")
    bashrc_path = os.path.join(base_path, "config_maps/bash-rc")
    init_script_path = os.path.join(base_path, "config_maps/init.sh")

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
