import click


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
