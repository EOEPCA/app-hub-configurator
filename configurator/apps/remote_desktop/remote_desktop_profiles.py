
import os
from configurator.apps.remote_desktop import BaseRemoteDesktopProfile

class NoVncDesktopProfile(BaseRemoteDesktopProfile):
    display_name = "Remote Desktop"
    description = "Linux desktop environment via web browser (noVNC)"
    slug = "remote_desktop"

    base_path = os.path.dirname(__file__)
    bash_login_path = os.path.join(base_path, "config_maps/bash-login")
    bashrc_path = os.path.join(base_path, "config_maps/bash-rc")
    init_script_path = os.path.join(base_path, "config_maps/init.sh")

    # noVNC entrypoint
    default_url = "/vnc.html"