import click


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
            try:
                value = int(raw)
            except ValueError as e:
                raise click.UsageError(
                    f"Invalid value for {field} in profile '{profile.slug}': {raw!r} "
                    "(must be an integer)"
                ) from e

        else:
            value = raw

        setattr(profile, field, value)
