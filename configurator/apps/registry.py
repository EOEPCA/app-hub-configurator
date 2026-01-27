from typing import Dict, Type

from configurator.apps.base import BaseAppProfile


class ProfileRegistry:
    def __init__(self):
        self._profiles: Dict[str, Type[BaseAppProfile]] = {}

    def register(self, profile_cls: Type[BaseAppProfile]) -> None:
        slug = profile_cls.slug

        if not slug:
            raise ValueError(f"{profile_cls.__name__} must define a non-empty slug")

        if slug in self._profiles:
            raise ValueError(
                f"Duplicate profile slug '{slug}' ({profile_cls.__name__})"
            )

        self._profiles[slug] = profile_cls

    def get(self, slug: str) -> Type[BaseAppProfile]:
        try:
            return self._profiles[slug]
        except KeyError:
            raise KeyError(f"Unknown profile slug '{slug}'")

    def all(self) -> Dict[str, Type[BaseAppProfile]]:
        return dict(self._profiles)
