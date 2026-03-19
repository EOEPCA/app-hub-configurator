import sys
import importlib
import pkgutil
import click
from pathlib import Path


def _import_or_reload(module_name: str) -> None:
    """
    Import a module and force execution of its module-level registration code.
    """
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    else:
        importlib.import_module(module_name)


def load_builtin_profiles():
    # Force built-in profile modules to execute registration code every run.
    for module_name in (
        "configurator.apps.coder",
        "configurator.apps.remote_desktop",
        "configurator.apps.jupyterlab",
    ):
        _import_or_reload(module_name)


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

        # Import all top-level modules/packages in that folder.
        # Drop cache first so profile registration runs even if module was
        # imported in a previous CLI invocation.
        for mod in pkgutil.iter_modules([str(p)]):
            sys.modules.pop(mod.name, None)
            importlib.import_module(mod.name)
