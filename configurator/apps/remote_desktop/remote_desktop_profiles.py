import os
from configurator.apps.remote_desktop import BaseRemoteDesktopProfile
from configurator.apps.app_helpers import get_config_map


class DesktopProfile(BaseRemoteDesktopProfile):
    display_name = "Remote Desktop"
    description = "Linux desktop environment via web browser (noVNC)"
    slug = "remote_desktop"

    base_path = os.path.dirname(__file__)
    bash_login_path = os.path.join(base_path, f"config_maps/{slug}/bash-login")
    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")


class DesktopQgisProfile(BaseRemoteDesktopProfile):
    display_name = "QGIS Remote Desktop"
    description = "Linux desktop environment with QGIS via web browser"
    slug = "qgis_remote_desktop"

    image = "ghcr.io/eoepca/iga-remote-desktop-qgis:latest"

    base_path = os.path.dirname(__file__)
    bash_login_path = os.path.join(base_path, f"config_maps/{slug}/bash-login")
    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")

    def get_config_maps(self) -> list:
        config_maps = []
        return super().get_config_maps() + config_maps

class DesktopPanoplyProfile(BaseRemoteDesktopProfile):
    display_name = "Panoply Remote Desktop"
    description = "Linux desktop environment with Panoply via web browser"
    slug = "panoply_remote_desktop"

    image = "ghcr.io/eoepca/iga-remote-desktop-panoply:latest-dev"

    base_path = os.path.dirname(__file__)
    bash_login_path = os.path.join(base_path, f"config_maps/{slug}/bash-login")
    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")

class DesktopSnapProfile(BaseRemoteDesktopProfile):
    display_name = "Snap Remote Desktop"
    description = "Linux desktop environment with Snap via web browser"
    slug = "snap_remote_desktop"

    image = "ghcr.io/eoepca/iga-remote-desktop-snap:latest-dev"

    base_path = os.path.dirname(__file__)
    bash_login_path = os.path.join(base_path, f"config_maps/{slug}/bash-login")
    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")

    snap_conf = get_config_map(
        path=os.path.join(base_path, f"config_maps/{slug}/snap12.conf"),
        slug=slug,
        name="snap-conf",
        key="snap.conf",
        mount_path="/usr/local/snap/etc/snap.conf",
        default_mode="0644",
        persist=False,
    )

    snap_properties = get_config_map(
        path=os.path.join(base_path, f"config_maps/{slug}/snap12.properties"),
        slug=slug,
        name="snap-properties",
        key="snap.properties",
        mount_path="/usr/local/snap/etc/snap.properties",
        default_mode="0644",
        persist=False,
    )

    def get_config_maps(self) -> list:
        config_maps = [self.snap_conf, self.snap_properties]
        return super().get_config_maps() + config_maps

    def get_pod_env_vars(self) -> dict:
        env = {
            **super().get_pod_env_vars(),
            "LIBGL_ALWAYS_SOFTWARE": "1",
            "HOME": "/workspace",
        }

        return env


