import sys
import importlib
import pkgutil
import click
from pathlib import Path


def load_builtin_profiles():
    # Trigger profile registration, set noqa to avoid unused import warning
    import configurator.apps.coder  # noqa: F401
    import configurator.apps.remote_desktop  # noqa: F401
    import configurator.apps.jupyterlab  # noqa: F401


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
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))

        # Import all top-level modules/packages in that folder
        for mod in pkgutil.iter_modules([str(p)]):
            importlib.import_module(mod.name)
