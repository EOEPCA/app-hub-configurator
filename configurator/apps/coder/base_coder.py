import os
from configurator.models import (
    Volume,
    VolumeMount,
    RoleBinding,
    Role,
    Subject,
    Verb,
)
from configurator.apps.base import BaseAppProfile


class BaseCoderProfile(BaseAppProfile):
    home_dir = "/workspace"

    image = "ghcr.io/eoepca/pde-code-server:latest-dev"

    base_path = os.path.dirname(__file__)
    manifests_path = os.path.join(base_path, "manifests")

    bash_login_path = os.path.join(base_path, "config_maps/common/bash-login")

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
            name=f"pod-manager-role-{self.slug.replace('_', '-')}",
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
            name=f"pod-exec-role-{self.slug.replace('_', '-')}",
            api_groups=[""],
            resources=["pods/exec"],
            verbs=[Verb.create],
        )

        log_reader_role = Role(
            name=f"log-reader-role-{self.slug.replace('_', '-')}",
            api_groups=[""],
            resources=["pods", "pods/log"],
            verbs=[
                Verb.get,
                Verb.list,
                Verb.watch,
            ],
        )

        job_submitter_role = Role(
            name=f"job-submitter-role-{self.slug.replace('_', '-')}",
            api_groups=["batch"],
            resources=["jobs"],
            verbs=[Verb.create, Verb.delete, Verb.list, Verb.watch, Verb.get],
        )

        bindings = [
            RoleBinding(
                name=f"log-reader-role-binding-{self.slug.replace('_', '-')}",
                subjects=[Subject(name="default", kind="ServiceAccount")],
                role=log_reader_role,
                persist=False,
            ),
            RoleBinding(
                name=f"pod-reader-role-binding-{self.slug.replace('_', '-')}",
                subjects=[Subject(name="default", kind="ServiceAccount")],
                role=pod_manager_role,
                persist=False,
            ),
            RoleBinding(
                name=f"pod-exec-role-binding-{self.slug.replace('_', '-')}",
                subjects=[Subject(name="default", kind="ServiceAccount")],
                role=pod_exec_role,
                persist=False,
            ),
            RoleBinding(
                name=f"job-submitter-role-binding-{self.slug.replace('_', '-')}",
                subjects=[Subject(name="default", kind="ServiceAccount")],
                role=job_submitter_role,
                persist=False,
            ),
        ]

        return super().get_role_bindings() + bindings
