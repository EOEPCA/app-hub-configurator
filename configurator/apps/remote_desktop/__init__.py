from configurator.apps import profile_registry
from .base_remote_desktop import BaseRemoteDesktopProfile
from .remote_desktop_profiles import NoVncDesktopProfile

__all__ = [
    "BaseRemoteDesktopProfile",
    "NoVncDesktopProfile",
]

profile_registry.register(NoVncDesktopProfile)