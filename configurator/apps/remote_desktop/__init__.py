from configurator.apps import profile_registry
from .base_remote_desktop import BaseRemoteDesktopProfile
from .remote_desktop_profiles import DesktopProfile, DesktopQgisProfile, DesktopPanoplyProfile
__all__ = [
    "BaseRemoteDesktopProfile",
    "DesktopProfile",
    "DesktopQgisProfile",
    "DesktopPanoplyProfile",
]

profile_registry.register(DesktopProfile)
profile_registry.register(DesktopQgisProfile)
profile_registry.register(DesktopPanoplyProfile)