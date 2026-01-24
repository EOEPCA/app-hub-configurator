from typing import List, Optional

from configurator.models import (
    Profile,
    ProfileDefinition,
    KubespawnerOverride,
    Volume,
)
from configurator.apps.app_helpers import (
    get_bash_login_config_map,
    get_bashrc_config_map,
    get_init_script_config_map,
    create_init_container,
)


class BaseAppProfile:
    # ---- required identity (must be overridden) ----
    display_name: str = ""
    description: str = ""
    slug: str = ""

    # --- image ----
    image: str

    default_url: str | None = None

    # ---- resources (sane defaults) ----
    cpu_guarantee: int = 1
    cpu_limit: int = 1
    mem_guarantee: str = "1G"
    mem_limit: str = "1G"

    workspace_volume_size = "20Gi"
    calrissian_volume_size = "50Gi"

    # ---- optional shell / init ----
    bash_login_path: Optional[str] = None
    bashrc_path: Optional[str] = None
    init_script_path: Optional[str] = None

    # ---- environment ----
    pod_env_vars: dict = {}

    def __init__(
        self,
        *,
        image: Optional[str] = None,
        storage_class_rwo: str | None = None,
        storage_class_rwx: str | None = None,
        volumes: Optional[List[Volume]] = None,
        groups,
        role_bindings=None,
        image_pull_secrets=None,
        node_selector=None,
    ):
        if storage_class_rwo:
            self.storage_class_rwo = storage_class_rwo
        if storage_class_rwx:
            self.storage_class_rwx = storage_class_rwx
        self.image = image or self.image
        self.volumes = volumes
        self.groups = groups
        self.role_bindings = role_bindings or []
        self.image_pull_secrets = image_pull_secrets or []
        self.node_selector = node_selector or {}
        
        user_volumes = volumes or []
        self.volumes = self.get_default_volumes() + user_volumes



    # ---- hooks -------------------------------------------------

    def get_pod_env_vars(self) -> dict:
        return self.pod_env_vars

    def get_extra_resource_limits(self) -> dict:
        return {}

    def get_default_volumes(self) -> list[Volume]:
        return []

    # ---- internals --------------------------------------------

    def _build_config_maps(self):
        cms = []

        if self.bash_login_path:
            cms.append(get_bash_login_config_map(self.bash_login_path))

        if self.bashrc_path:
            cms.append(get_bashrc_config_map(self.bashrc_path))

        return cms

    def _build_init(self):
        if not self.init_script_path:
            return [], []

        cm = get_init_script_config_map(self.init_script_path)
        if not cm:
            return [], []

        init = create_init_container(
            image=self.image,
            volume_mounts=[v.volume_mount for v in self.volumes],
        )

        return [cm], [init]

    # ---- public API -------------------------------------------

    def build(self) -> Profile:
        if not self.slug:
            raise ValueError("Profile slug must be defined")

        config_maps = self._build_config_maps()
        init_cms, init_containers = self._build_init()
        config_maps.extend(init_cms)

        profile = Profile(
            id=f"profile_{self.slug}",
            groups=self.groups,
            definition=ProfileDefinition(
                display_name=self.display_name,
                description=self.description,
                slug=self.slug,
                default=False,
                kubespawner_override=KubespawnerOverride(
                    cpu_guarantee=self.cpu_guarantee,
                    cpu_limit=self.cpu_limit,
                    mem_guarantee=self.mem_guarantee,
                    mem_limit=self.mem_limit,
                    image=self.image,
                ),
            ),
            default_url=self.default_url,
            node_selector=self.node_selector,
            volumes=self.volumes,
            config_maps=config_maps,
            init_containers=init_containers,
            role_bindings=self.role_bindings,
            image_pull_secrets=self.image_pull_secrets,
            pod_env_vars=self.get_pod_env_vars(),
        )

        extra = self.get_extra_resource_limits()
        if extra:
            profile.definition.kubespawner_override.extra_resource_limits = extra

        return profile