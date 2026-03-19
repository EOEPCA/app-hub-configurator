import os

from configurator.apps import profile_registry
from configurator.apps.app_helpers import get_config_map
from configurator.apps.coder.base_coder import BaseCoderProfile
from configurator.models import ImagePullSecret, Role, RoleBinding, Subject, Verb


class EoepcaBaseCoderProfile(BaseCoderProfile):
    image = "ghcr.io/eoepca/pde-code-server:latest-dev"
    storage_class_rwo = "standard"
    storage_class_rwx = "standard"

    base_path = os.path.dirname(__file__)
    copy_secrets_path = os.path.join(base_path, "config_maps/common/copy-secrets")

    def get_image_pull_secrets(self) -> list[ImagePullSecret]:
        return [
            ImagePullSecret(
                name="incluster-cr-secret",
                persist=False,
                data="ewoJImF1dGhzIjogewoJCSJjci50ZXJyYWR1ZS5jb20iOiB7CgkJCSJhdXRoIjogIlptSnlhWFJ2T21ZNVZFNUNaVTlIVEE9PSIKCQl9Cgl9Cn0=",
            )
        ] + super().get_image_pull_secrets()

    def get_config_maps(self):
        config_maps = [
            get_config_map(
                slug=self.slug,
                path=self.copy_secrets_path,
                name="copy-secrets",
                key="copy-secrets",
                mount_path="/usr/bin/copy-secrets",
                default_mode="0755",
                persist=False,
            )
        ]

        return super().get_config_maps() + config_maps

    def get_pod_env_vars(self) -> dict:
        return {
            **super().get_pod_env_vars(),
            "NAMESPACE": "{{ namespace }}",
        }

    def get_role_bindings(self) -> list[RoleBinding]:
        secret_patcher_role = Role(
            name=f"secret-patcher-role-{self.slug.replace('_', '-')}",
            api_groups=[""],
            resources=["secrets"],
            verbs=[Verb.create, Verb.delete],
        )

        binding = RoleBinding(
            name=f"secret-patcher-role-binding-{self.slug.replace('_', '-')}",
            subjects=[Subject(name="default", kind="ServiceAccount")],
            role=secret_patcher_role,
            persist=False,
        )

        return super().get_role_bindings() + [binding]


class EoepcaCoderProfile(EoepcaBaseCoderProfile):
    slug = "eoepca_coder_app"
    display_name = "EOEPCA Code Server"
    description = "Code Server with EOEPCA-specific image pull secret handling"


class MlflowCoderProfile(EoepcaBaseCoderProfile):
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


class TrainingHowToProfile(EoepcaBaseCoderProfile):
    default_url = "/workspace/how-to"

    slug = "training_how_to_app"
    display_name = "Application Package CWL How-To's"
    description = (
        "Code Server configured for running the How-To's of the "
        "Application Packages using CWL"
    )

    workspace_volume_size = "15Gi"
    calrissian_volume_size = "30Gi"

    storage_class_rwo = "standard"
    storage_class_rwx = "standard"

    base_path = os.path.dirname(__file__)
    bash_login_path = os.path.join(base_path, f"config_maps/{slug}/bash-login")
    bashrc_path = os.path.join(base_path, f"config_maps/{slug}/bash-rc")
    init_script_path = os.path.join(base_path, f"config_maps/{slug}/init.sh")

    def get_pod_env_vars(self) -> dict:
        return {
            **super().get_pod_env_vars(),
            "CODE_SERVER_WS": "/workspace/how-to",
        }


profile_registry.register(EoepcaCoderProfile)
profile_registry.register(MlflowCoderProfile)
profile_registry.register(TrainingHowToProfile)
