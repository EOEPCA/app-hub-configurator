# SPDX-FileCopyrightText: 2024-present Fabrice Brito <fabrice.brito@terradue.com>
#
# SPDX-License-Identifier: MIT

from configurator.apps import profile_registry
from .base_coder import BaseCoderProfile
from .coder_profiles import CoderProfile, GpuCoderProfile, DaskGatewayCoderProfile
from .training_profiles import TrainingHowToProfile

__all__ = [
    "BaseCoderProfile",
    "CoderProfile",
    "GpuCoderProfile",
    "DaskGatewayCoderProfile",
    "TrainingHowToProfile",
]

profile_registry.register(CoderProfile)
profile_registry.register(GpuCoderProfile)
profile_registry.register(DaskGatewayCoderProfile)
profile_registry.register(TrainingHowToProfile)
