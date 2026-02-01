from typing import Dict, Type

from configurator.apps.base import BaseAppProfile

import click


class ProfileRegistry:
    def __init__(self):
        """Registry for application profiles.

        Args:
            None
        """
        self._profiles: Dict[str, Type[BaseAppProfile]] = {}

    def clear(self) -> None:
        """Clear all registered profiles.

        Args:
            None
        """
        self._profiles.clear()

    def register(self, profile_cls: Type[BaseAppProfile]) -> None:
        """Register a profile class.

        Args:
            profile_cls: The profile class to register.
        """
        slug = profile_cls.slug

        if not slug:
            raise ValueError(f"{profile_cls.__name__} must define a non-empty slug")

        if slug in self._profiles:
            raise ValueError(
                f"Duplicate profile slug '{slug}' ({profile_cls.__name__})"
            )

        self._profiles[slug] = profile_cls

    def get(self, slug: str) -> Type[BaseAppProfile]:
        """Get a registered profile class by slug.

        Args:
            slug: The slug of the profile to retrieve.
        Returns:
            The profile class associated with the given slug.
        """
        try:
            return self._profiles[slug]
        except KeyError as e:
            raise click.UsageError(f"Unknown profile slug '{slug}'") from e

    def all(self) -> Dict[str, Type[BaseAppProfile]]:
        """Get all registered profiles.

        Args:
            None
        """
        return dict(self._profiles)
