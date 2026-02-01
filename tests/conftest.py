import importlib

import pytest

from configurator.apps import profile_registry


@pytest.fixture(autouse=True)
def reset_registry():
    """
    Ensure registry is clean for every test.

    Also reload profile modules if needed.
    """
    profile_registry.clear()

    # Optional but often useful: reload modules so registration runs again
    # if modules were already imported in the Python process.
    # (Only needed if you keep module-level registration logic.)
    for mod in [
        "configurator.apps.coder",
        "configurator.apps.remote_desktop",
    ]:
        if mod in list(importlib.sys.modules):
            importlib.reload(importlib.import_module(mod))

    yield

    # clean again at end (optional)
    profile_registry.clear()
