# main.py
import os
import yaml
import click

from configurator.apps import profile_registry
from configurator.models import Config

# Trigger profile registration
import configurator.apps.coder
import configurator.apps.remote_desktop


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
                f"Invalid --node-selector '{item}'. "
                "Expected <slug>:<key>=<value>"
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
                f"Invalid --override '{item}'. "
                "Expected <slug>:<field>=<value>"
            )

        result.setdefault(slug, {})[key] = value

    return result


def apply_overrides(profile, overrides: dict[str, str]) -> None:
    for field, raw in overrides.items():
        if not hasattr(profile, field):
            raise click.UsageError(
                f"Unknown override field '{field}' "
                f"for profile '{profile.slug}'"
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
        "Override profile attributes. "
        "Format: <slug>:<field>=<value>. "
        "Can be repeated."
    ),
)
def main(profiles: str, groups: str, output: str, storage_class_rwo: str, storage_class_rwx: str, node_selector: list[str], override: list[str]):
    """
    Generate an application-hub configuration YAML.
    """

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

    with open(output, "w") as f:
        yaml.safe_dump(
            config.model_dump(exclude_none=True),
            f,
            sort_keys=False,
        )

    click.echo(f"Config written to {output}")


if __name__ == "__main__":
    main()
