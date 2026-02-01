import click


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
