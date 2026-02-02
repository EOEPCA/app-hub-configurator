# SPDX-FileCopyrightText: 2024-present Fabrice Brito <fabrice.brito@terradue.com>
#
# SPDX-License-Identifier: MIT

from configurator.apps import profile_registry
from .jupyterlab_profiles import JupyterLabSmallProfile

__all__ = [
    "JupyterLabSmallProfile",
]

profile_registry.register(JupyterLabSmallProfile)
