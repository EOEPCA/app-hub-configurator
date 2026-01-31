import os
from configurator.apps.coder import BaseCoderProfile
from configurator.apps.app_helpers import load_manifests


class CoderProfile(BaseCoderProfile):
    display_name = "Code Server"
    description = "Code Server for development"
    slug = "coder_app"

    workspace_volume_size = "10Gi"
    calrissian_volume_size = "25Gi"

    storage_class_rwo = "standard"
    storage_class_rwx = "standard"

    base_path = os.path.dirname(__file__)
    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")

    def get_manifests(self):
        return super().get_manifests() + [
            load_manifests(
                slug=self.slug,
                name=f"local-stack-{self.slug.replace('_', '-')}",
                key="local-stack",
                file_path=os.path.join(
                    self.manifests_path,
                    self.slug,
                    "local-stack.yaml",
                ),
            )
        ]
    
    def get_env_secrets(self) -> list[str]:
        return ["localstack-s3-secret-coder-app"] + super().get_env_secrets()

    def get_env_config_maps(self) -> list[str]:
        return ["env-var-configmap-coder-app"] + super().get_env_config_maps()

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


class DaskGatewayCoderProfile(BaseCoderProfile):
    default_url = "/workspace/dask-app-package"

    display_name = "Code Server with Dask Gateway"
    description = "Code Server with Dask Gateway for distributed computing"
    slug = "coder_dask_gateway_app"

    workspace_volume_size = "15Gi"
    calrissian_volume_size = "30Gi"

    storage_class_rwo = "standard"
    storage_class_rwx = "standard"

    base_path = os.path.dirname(__file__)

    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")

    def get_pod_env_vars(self) -> dict:
        env = {
            **super().get_pod_env_vars(),
            "DASK_GATEWAY_ADDRESS": "http://traefik-dask-gw-jupyter-{{ spawner.user.name }}-dask-gateway.{{ namespace }}.svc.cluster.local:80",
            "CODE_SERVER_WS": "/workspace/dask-app-package",
        }

        return env

    def get_manifests(self):
        return super().get_manifests() + [
            load_manifests(
                name="dask-gateway",
                key="dask-gateway",
                slug=self.slug,
                file_path=os.path.join(
                    self.manifests_path,
                    self.slug,
                    "dask-gateway.yaml",
                ),
            )
        ]
