# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# Disable E0213 because resolvers are staticmethod in disguise
# pylint: disable=no-self-argument
# Disable flake8 on all file in order to disable B902.
# Unfortunately not possible to disable only a specific warning for the whole file
# flake8: noqa

import graphene

from .types.environment import Environment
from .types.mandate import (
    ext_mandates,
    int_mandates,
    resolve_ext_mandates,
    resolve_int_mandates,
    resolve_sta_mandates,
    sta_mandates,
)
from .types.power_level import (
    int_power_levels,
    resolve_int_power_levels,
    resolve_sta_power_levels,
    sta_power_levels,
)


class Query(graphene.ObjectType):
    environment = graphene.Field(
        Environment, description="Information about the server."
    )
    int_mandates = int_mandates
    ext_mandates = ext_mandates
    sta_mandates = sta_mandates
    int_power_levels = int_power_levels
    sta_power_levels = sta_power_levels

    def resolve_environment(root, info):
        return Environment()

    def resolve_int_mandates(root, info, limit=None, offset=0):
        return resolve_int_mandates(info, limit, offset)

    def resolve_ext_mandates(root, info, limit=None, offset=0):
        return resolve_ext_mandates(info, limit, offset)

    def resolve_sta_mandates(root, info, limit=None, offset=0):
        return resolve_sta_mandates(info, limit, offset)

    def resolve_int_power_levels(root, info, ids=None, name=None, limit=None, offset=0):
        return resolve_int_power_levels(info, ids, name, limit, offset)

    def resolve_sta_power_levels(root, info, ids=None, name=None, limit=None, offset=0):
        return resolve_sta_power_levels(info, ids, name, limit, offset)


schema = graphene.Schema(query=Query)
