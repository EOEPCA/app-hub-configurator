import os
from configurator.apps.jupyterlab.base_jupyterlab import BaseJupyterLabProfile


class JupyterLabSmallProfile(BaseJupyterLabProfile):
    slug = "jupyterlab_small"

    base_path = os.path.dirname(__file__)
    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")

    display_name = "JupyterLab Small"
    description = "JupyterLab environment with essential data science tools"
