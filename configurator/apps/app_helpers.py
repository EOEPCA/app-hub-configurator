from configurator.models import (
    ConfigMap,
    InitContainer,
    VolumeMount,
    InitContainerVolumeMount,
    Manifest,
)
from typing import List
from ruamel.yaml.scalarstring import LiteralScalarString
import yaml


def literal(s: str):
    return LiteralScalarString(s)


def literalize_multiline(obj):
    """
    Recursively wrap multiline strings as LiteralScalarString.
    """
    if isinstance(obj, str):
        if "\n" in obj:
            return LiteralScalarString(obj)
        return obj

    if isinstance(obj, list):
        return [literalize_multiline(i) for i in obj]

    if isinstance(obj, dict):
        return {k: literalize_multiline(v) for k, v in obj.items()}

    return obj


def create_init_container(
    image: str, volume_mounts: List[VolumeMount]
) -> InitContainer:
    init_context_volume_mount = InitContainerVolumeMount(
        mount_path="/opt/init/.init.sh", name="init", sub_path="init"
    )

    return InitContainer(
        name="init-file-on-volume",
        image=image,
        command=["sh", "-c", "sh /opt/init/.init.sh"],
        volume_mounts=[
            *volume_mounts,
            init_context_volume_mount,
        ],
    )


def get_config_map(
    path: str,
    name: str,
    key: str,
    mount_path: str,
    readonly: bool = True,
    persist: bool = True,
    default_mode: str = "0660",
) -> ConfigMap:
    try:
        with open(path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(
            f"Warning: Config map file {name} not found in {path}/config_maps/. Skipping."
        )
        return None

    return ConfigMap(
        name=name,
        key=key,
        content=content,
        readonly=readonly,
        persist=persist,
        mount_path=mount_path,
        default_mode=default_mode,
    )


def get_bash_login_config_map(
    path: str, readonly: bool = True, persist: bool = True
) -> ConfigMap:
    return get_config_map(
        path=path,
        name="bash-login",
        key="bash-login",
        mount_path="/workspace/.bash_login",
        readonly=readonly,
        persist=persist,
        default_mode="0660",
    )


def get_bashrc_config_map(
    path: str, readonly: bool = True, persist: bool = True
) -> ConfigMap:
    return get_config_map(
        path=path,
        name="bash-rc",
        key="bash-rc",
        mount_path="/workspace/.bashrc",
        readonly=readonly,
        persist=persist,
        default_mode="0660",
    )


def get_init_script_config_map(
    path: str, readonly: bool = True, persist: bool = True
) -> ConfigMap:
    return get_config_map(
        path=path,
        name="init",
        key="init",
        readonly=readonly,
        persist=persist,
        mount_path="/opt/init/.init.sh",
        default_mode="0660",
    )


def load_manifests(*, name: str, key: str, file_path: str) -> Manifest:
    with open(file_path, "r") as f:
        content = list(yaml.safe_load_all(f))

    # Remove empty docs caused by ---
    content = [doc for doc in content if doc is not None]

    return Manifest(
        name=name,
        key=key,
        persist=False,
        content=content,
    )
