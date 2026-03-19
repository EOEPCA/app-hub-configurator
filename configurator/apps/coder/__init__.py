# SPDX-FileCopyrightText: 2024-present Fabrice Brito <fabrice.brito@terradue.com>
#
# SPDX-License-Identifier: MIT

from configurator.apps import profile_registry
from .base_coder import BaseCoderProfile
from .coder_profiles import CoderProfile, GpuCoderProfile, DaskGatewayCoderProfile

__all__ = [
    "BaseCoderProfile",
    "CoderProfile",
    "GpuCoderProfile",
    "DaskGatewayCoderProfile",
]

profile_registry.register(CoderProfile)
profile_registry.register(GpuCoderProfile)
profile_registry.register(DaskGatewayCoderProfile)
