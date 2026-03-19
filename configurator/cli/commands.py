import click
from configurator.apps import (
    profile_registry,
)
from configurator.plugins.loader import load_builtin_profiles, load_external_profiles
from configurator.describe.profile import describe
from configurator.models import Config
from configurator.overrides.apply import apply_overrides
from configurator.overrides.parser import (
    parse_node_selector_overrides,
    parse_overrides,
    split_csv,
)
from configurator.io.yaml_writer import write_yaml


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
    # Build a fresh registry snapshot for each CLI invocation.
    profile_registry.clear()

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
            node_selector=node_selector_overrides.get(slug, {}),
        )
        if slug in override_map:
            apply_overrides(profile, override_map[slug])
        profiles_out.append(profile.build())

    config = Config(profiles=profiles_out)

    write_yaml(config, output)

    click.echo(f"Config written to {output}")
