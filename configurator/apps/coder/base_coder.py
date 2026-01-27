import os
from configurator.models import Volume, VolumeMount, RoleBinding, Role, Subject, Verb, ImagePullSecret
from configurator.apps.base import BaseAppProfile
from configurator.apps.app_helpers import get_config_map


class BaseCoderProfile(BaseAppProfile):
    home_dir = "/workspace"

    image = "ghcr.io/eoepca/pde-code-server:latest-dev"

    base_path = os.path.dirname(__file__)
    manifests_path = os.path.join(base_path, "manifests")

    bash_login_path = os.path.join(base_path, f"config_maps/common/bash-login")
    copy_secrets = os.path.join(base_path, f"config_maps/common/copy-secrets")

    def get_image_pull_secrets(self) -> list[str]:
        incluster_image_pull_secret = ImagePullSecret(
            name="incluster-cr-secret",
            persist=False,
            data="ewoJImF1dGhzIjogewoJCSJjci50ZXJyYWR1ZS5jb20iOiB7CgkJCSJhdXRoIjogIlptSnlhWFJ2T21ZNVZFNUNaVTlIVEE9PSIKCQl9Cgl9Cn0=",
        )

        return [incluster_image_pull_secret] + super().get_image_pull_secrets()

    def get_config_maps(self):
        config_maps = [
            get_config_map(
                path=self.copy_secrets,
                name="copy-secrets",
                key="copy-secrets",
                mount_path="/usr/bin/copy-secrets",
                default_mode="755",
                persist=False,
            ),
        ]

        return super().get_config_maps() + config_maps

    def get_default_volumes(self) -> list[Volume]:
        return [
            Volume(
                name="calrissian-volume",
                claim_name="calrissian-claim",
                size=self.calrissian_volume_size,
                storage_class=self.storage_class_rwx,
                access_modes=["ReadWriteMany"],
                volume_mount=VolumeMount(
                    name="calrissian-volume", mount_path="/calrissian"
                ),
                persist=False,
            ),
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

    pod_env_vars = {
        "HOME": home_dir,
        "XDG_RUNTIME_DIR": f"{home_dir}/.local",
        "XDG_CONFIG_HOME": f"{home_dir}/.local",
        "XDG_DATA_HOME": f"{home_dir}/.local/share/",
        "CWLTOOL_OPTIONS": "--podman",
        "NAMESPACE": "{{ namespace }}",
    }

    def get_manifests(self):
        return []

    # coder defaults
    cpu_guarantee = 1
    cpu_limit = 2
    mem_guarantee = "4G"
    mem_limit = "6G"

    def get_role_bindings(self) -> list[RoleBinding]:
        pod_manager_role = Role(
            name="pod-manager-role",
            api_groups=[""],
            resources=["pods"],
            verbs=[
                Verb.create,
                Verb.patch,
                Verb.delete,
                Verb.list,
                Verb.watch,
                Verb.get,
            ],
        )

        pod_exec_role = Role(
            name="pod-exec-role",
            api_groups=[""],
            resources=["pods/exec"],
            verbs=[Verb.create],
        )

        log_reader_role = Role(
            name="log-reader-role",
            api_groups=[""],
            resources=["pods", "pods/log"],
            verbs=[
                Verb.get,
                Verb.list,
                Verb.watch,
            ],
        )

        secret_patcher_role = Role(
            name="secret-patcher-role",
            api_groups=[""],
            resources=["secrets"],
            verbs=[Verb.create, Verb.delete],
        )

        job_submitter_role = Role(
            name="job-submitter-role",
            api_groups=["batch"],
            resources=["jobs"],
            verbs=[Verb.create, Verb.delete, Verb.list, Verb.watch, Verb.get],
        )

        bindings = [
            RoleBinding(
                name="log-reader-role-binding",
                subjects=[Subject(name="default", kind="ServiceAccount")],
                role=log_reader_role,
                persist=False,
            ),
            RoleBinding(
                name="pod-reader-role-binding",
                subjects=[Subject(name="default", kind="ServiceAccount")],
                role=pod_manager_role,
                persist=False,
            ),
            RoleBinding(
                name="pod-exec-role-binding",
                subjects=[Subject(name="default", kind="ServiceAccount")],
                role=pod_exec_role,
                persist=False,
            ),
            RoleBinding(
                name="secret-patcher-role-binding",
                subjects=[Subject(name="default", kind="ServiceAccount")],
                role=secret_patcher_role,
                persist=False,
            ),
            RoleBinding(
                name="job-submitter-role-binding",
                subjects=[Subject(name="default", kind="ServiceAccount")],
                role=job_submitter_role,
                persist=False,
            ),
        ]

        return super().get_role_bindings() + bindings
