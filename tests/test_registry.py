import pytest
import click

from configurator.apps.registry import ProfileRegistry
from configurator.apps.base import BaseAppProfile


def make_profile(slug: str):
    """
    Helper: dynamically create a minimal profile class.
    """

    class _P(BaseAppProfile):
        pass

    _P.slug = slug
    _P.display_name = f"Profile {slug}"
    _P.description = f"Description {slug}"
    _P.image = "dummy:latest"

    return _P


def test_registry_register_and_get():
    reg = ProfileRegistry()

    P = make_profile("coder_app")
    reg.register(P)

    assert reg.get("coder_app") is P


def test_registry_get_unknown_slug_raises_click_usageerror():
    reg = ProfileRegistry()

    with pytest.raises(click.UsageError) as e:
        reg.get("does_not_exist")

    assert "Unknown profile slug" in str(e.value)
    assert "does_not_exist" in str(e.value)


def test_registry_register_requires_non_empty_slug():
    reg = ProfileRegistry()

    P = make_profile("")
    with pytest.raises(ValueError) as e:
        reg.register(P)

    assert "must define a non-empty slug" in str(e.value)


def test_registry_register_duplicate_slug_raises():
    reg = ProfileRegistry()

    P1 = make_profile("coder_app")
    P2 = make_profile("coder_app")

    reg.register(P1)

    with pytest.raises(ValueError) as e:
        reg.register(P2)

    assert "Duplicate profile slug" in str(e.value)
    assert "coder_app" in str(e.value)


def test_registry_all_returns_copy_not_reference():
    reg = ProfileRegistry()

    P = make_profile("coder_app")
    reg.register(P)

    data = reg.all()
    assert data["coder_app"] is P

    # modifying returned dict should not affect registry
    data.clear()

    assert "coder_app" in reg.all()


def test_registry_clear_removes_all():
    reg = ProfileRegistry()

    reg.register(make_profile("coder_app"))
    reg.register(make_profile("gpu_coder_app"))

    assert len(reg.all()) == 2

    reg.clear()

    assert reg.all() == {}
