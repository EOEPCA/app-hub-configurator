from configurator.apps import profile_registry
from configurator.apps.coder.base_coder import BaseCoderProfile


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


profile_registry.register(MlflowCoderProfile)
