# main.py
import click
from configurator.apps import profile_registry
from configurator.models import Config

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from ruamel.yaml.representer import SafeRepresenter
import sys
import importlib
import pkgutil
from pathlib import Path


def load_builtin_profiles():
    # Trigger profile registration, set noqa to avoid unused import warning
    import configurator.apps.coder  # noqa: F401
    import configurator.apps.remote_desktop  # noqa: F401

def load_external_profiles(profile_dirs: tuple[str, ...]) -> None:
    """
    Load external profile python modules/packages from given directories.

    Each directory is added to sys.path and all top-level modules/packages
    in that directory are imported.

    The imported modules are expected to register profiles into profile_registry.
    """
    for d in profile_dirs:
        p = Path(d).resolve()

        if not p.exists() or not p.is_dir():
            raise click.UsageError(f"--profiles-dir must be an existing folder: {d}")

        # Make modules importable
        sys.path.insert(0, str(p))

        # Import all top-level modules/packages in that folder
        for mod in pkgutil.iter_modules([str(p)]):
            importlib.import_module(mod.name)

def literalize_multiline_values(obj):
    """
    Recursively wrap multiline *values* as LiteralScalarString.
    NEVER touch dict keys.
    """
    if isinstance(obj, list):
        return [literalize_multiline_values(i) for i in obj]

    if isinstance(obj, dict):
        return {k: literalize_multiline_values(v) for k, v in obj.items()}

    if isinstance(obj, str) and "\n" in obj:
        return LiteralScalarString(obj)

    return obj


def write_yaml(config: Config, output: str) -> None:
    yaml_writer = YAML(typ="safe", pure=True)
    yaml_writer.default_flow_style = False
    # set the line width to a large value to avoid unwanted line breaks
    yaml_writer.width = 4096

    yaml_writer.representer.add_representer(
        LiteralScalarString,
        SafeRepresenter.represent_str,
    )

    # Dump FIRST
    data = config.model_dump(exclude_none=True, mode="json")

    # THEN wrap multiline strings
    data = literalize_multiline_values(data)

    with open(output, "w") as f:
        yaml_writer.dump(data, f)


def split_csv(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def parse_node_selector_overrides(
    values: tuple[str, ...],
) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}

    for item in values:
        try:
            slug, rest = item.split(":", 1)
            key, value = rest.split("=", 1)
        except ValueError:
            raise click.UsageError(
                f"Invalid --node-selector '{item}'. Expected <slug>:<key>=<value>"
            )

        result.setdefault(slug, {})[key] = value
    print(result)
    return result


def parse_overrides(
    values: tuple[str, ...],
) -> dict[str, dict[str, str]]:
    """
    Returns:
      {
        "coder_app": {
          "cpu_limit": "4",
          "mem_limit": "8G",
        },
        "gpu_coder_app": {
          "image": "ghcr.io/..."
        }
      }
    """
    result: dict[str, dict[str, str]] = {}

    for item in values:
        try:
            slug, rest = item.split(":", 1)
            key, value = rest.split("=", 1)
        except ValueError:
            raise click.UsageError(
                f"Invalid --override '{item}'. Expected <slug>:<field>=<value>"
            )

        result.setdefault(slug, {})[key] = value

    return result


def apply_overrides(profile, overrides: dict[str, str]) -> None:
    for field, raw in overrides.items():
        if not hasattr(profile, field):
            raise click.UsageError(
                f"Unknown override field '{field}' for profile '{profile.slug}'"
            )

        if field == "groups":
            groups = [g.strip() for g in raw.split(",") if g.strip()]
            if not groups:
                raise click.UsageError(
                    f"groups override for '{profile.slug}' cannot be empty"
                )
            value = groups

        elif field in {"cpu_limit", "cpu_guarantee"}:
            value = int(raw)

        else:
            value = raw

        setattr(profile, field, value)


def describe(profile) -> None:
    click.echo()
    click.echo(f"Profile: {profile.slug}")
    click.echo("-" * (9 + len(profile.slug)))

    click.echo(f"Display name : {profile.display_name}")
    click.echo(f"Description  : {profile.description}")
    click.echo(f"Image        : {profile.image}")
    click.echo()

    click.echo("Resources:")
    click.echo(f"  CPU   : {profile.cpu_guarantee} → {profile.cpu_limit}")
    click.echo(f"  Memory: {profile.mem_guarantee} → {profile.mem_limit}")
    click.echo()

    volumes = profile.get_default_volumes()
    if volumes:
        click.echo("Volumes:")
        for v in volumes:
            mode = ",".join(v.access_modes)
            persist = "persistent" if v.persist else "transient"
            click.echo(f"  - {v.name} ({mode}, {v.size}, {persist})")
        click.echo()

    if profile.pod_env_vars:
        click.echo("Environment variables:")
        for k, v in profile.pod_env_vars.items():
            click.echo(f"  {k}={v}")
        click.echo()

    manifests = profile.get_manifests()
    if manifests:
        click.echo("Manifests:")
        for m in manifests:
            count = len(m.content) if m.content else 0
            click.echo(f"  - {m.name} ({count} resources)")
        click.echo()

    click.echo("Overrides:")
    click.echo(
        "  Supported: cpu_limit, cpu_guarantee, "
        "mem_limit, mem_guarantee, image, groups, node_selector"
    )


@click.command()
@click.option(
    "--profiles",
    envvar="ENABLED_PROFILES",
    default="coder_app",
    show_default=True,
    help="Comma-separated list of enabled profile slugs",
)
@click.option(
    "--groups",
    envvar="GROUPS",
    default="developers",
    show_default=True,
    help="Comma-separated list of groups",
)
@click.option(
    "--output",
    envvar="OUTPUT_FILE",
    default="config.yaml",
    show_default=True,
    help="Output YAML file",
)
@click.option(
    "--storage-class-rwo",
    envvar="STORAGE_CLASS_RWO",
    help="StorageClass for ReadWriteOnce volumes",
)
@click.option(
    "--storage-class-rwx",
    envvar="STORAGE_CLASS_RWX",
    help="StorageClass for ReadWriteMany volumes",
)
@click.option(
    "--node-selector",
    multiple=True,
    help=(
        "Override node selector for a profile. "
        "Format: <slug>:<key>=<value>. "
        "Can be repeated."
    ),
)
@click.option(
    "--override",
    multiple=True,
    help=(
        "Override profile attributes. Format: <slug>:<field>=<value>. Can be repeated."
    ),
)
@click.option(
    "--list-profiles",
    is_flag=True,
    help="List available registered profile slugs and exit",
)
@click.option(
    "--describe-profile",
    metavar="SLUG",
    help="Print a human-readable summary of a profile and exit",
)
@click.option(
    "--profiles-dir",
    multiple=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help=(
        "Extra folder(s) containing python modules/packages defining additional "
        "profiles. Modules must register into profile_registry."
    ),
)
def main(
    profiles: str,
    groups: str,
    output: str,
    storage_class_rwo: str,
    storage_class_rwx: str,
    node_selector: list[str],
    override: list[str],
    list_profiles: bool,
    describe_profile: str,
    profiles_dir: list[str],    
) -> None:
    """
    Generate an application-hub configuration YAML.
    """
    # Load built-in profiles FIRST
    load_builtin_profiles()

    # Load external profiles (plugins) BEFORE using profile_registry
    if profiles_dir:
        load_external_profiles(tuple(profiles_dir))

    if describe_profile:
        profile_cls = profile_registry.get(describe_profile)
        profile = profile_cls(
            volumes=[],
            groups=[],
            storage_class_rwo=None,
            storage_class_rwx=None,
            node_selector={},
        )
        describe(profile)
        raise SystemExit(0)

    if list_profiles:
        click.echo("Available profiles:")
        for slug, cls in profile_registry.all().items():
            display = getattr(cls, "display_name", "")
            if display:
                click.echo(f"  - {slug:25} {display}")
            else:
                click.echo(f"  - {slug}")
        raise SystemExit(0)

    enabled_slugs = split_csv(profiles)
    group_list = split_csv(groups)

    if not group_list:
        raise click.UsageError("At least one group must be specified")

    node_selector_overrides = parse_node_selector_overrides(node_selector)

    override_map = parse_overrides(override)

    profiles_out = []

    for slug in enabled_slugs:
        profile_cls = profile_registry.get(slug)
        profile = profile_cls(
            volumes=[],
            groups=group_list,
            storage_class_rwo=storage_class_rwo,
            storage_class_rwx=storage_class_rwx,
            node_selector=node_selector_overrides,
        )
        if slug in override_map:
            apply_overrides(profile, override_map[slug])
        profiles_out.append(profile.build())

    config = Config(profiles=profiles_out)

    write_yaml(config, output)

    click.echo(f"Config written to {output}")


if __name__ == "__main__":
    main()
