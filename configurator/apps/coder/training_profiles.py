import os
from configurator.apps.coder.base_coder import BaseCoderProfile


class TrainingHowToProfile(BaseCoderProfile):

    default_url = "/workspace/how-to"

    display_name = "Application Package CWL How-To's"
    description = "Code Server configured for running the How-To's of the Application Packages using CWL"
    slug = "training_how_to_app"

    workspace_volume_size = "15Gi"
    calrissian_volume_size = "30Gi"

    storage_class_rwo = "standard"
    storage_class_rwx = "standard"

    base_path = os.path.dirname(__file__)
    bash_login_path = os.path.join(base_path, f"config_maps/{slug}/bash-login")
    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")

    def get_pod_env_vars(self) -> dict:

        env = {**super().get_pod_env_vars(),            
                "CODE_SERVER_WS": "/workspace/how-to",
                }

        return env
