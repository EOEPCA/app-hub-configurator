
import os
from configurator.apps.coder import BaseCoderProfile

class CoderProfile(BaseCoderProfile):
    display_name = "Code Server"
    description = "Code Server for development"
    slug = "coder_app"

    workspace_volume_size = "10Gi"
    calrissian_volume_size = "25Gi"

    storage_class_rwo = "standard"
    storage_class_rwx = "standard"

    base_path = os.path.dirname(__file__)
    bash_login_path = os.path.join(base_path, f"config_maps/{slug}/bash-login")
    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")

class GpuCoderProfile(BaseCoderProfile):
    display_name = "GPU Code Server"
    description = "Code Server with GPU acceleration"
    slug = "gpu_coder_app"

    cpu_guarantee = 4
    cpu_limit = 8
    mem_guarantee = "16G"
    mem_limit = "32G"

    gpu_limit = 1

    storage_class_rwo = "standard"
    storage_class_rwx = "standard"

    workspace_volume_size = "20Gi"
    calrissian_volume_size = "50Gi"

    base_path = os.path.dirname(__file__)
    bash_login_path = os.path.join(base_path, f"config_maps/{slug}/bash-login")
    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")

    def __init__(self, *, node_selector=None, **kwargs):
        selector = {
            "nvidia.com/gpu.present": "true",
        }

        if node_selector:
            selector.update(node_selector)

        super().__init__(node_selector=selector, **kwargs)

    def get_extra_resource_limits(self):
        return {"nvidia.com/gpu": self.gpu_limit}