import os
from configurator.apps.remote_desktop import BaseRemoteDesktopProfile


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


class DesktopPanoplyProfile(BaseRemoteDesktopProfile):
    display_name = "Panoply Remote Desktop"
    description = "Linux desktop environment with Panoply via web browser"
    slug = "panoply_remote_desktop"

    base_path = os.path.dirname(__file__)
    bash_login_path = os.path.join(base_path, f"config_maps/{slug}/bash-login")
    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")
