# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# pylint: disable=no-self-argument
# flake8: noqa

import graphene

from odoo.addons.graphql_base import OdooObjectType

from . import instance
from .assembly_category import (
    ExtAssemblyCategory,
    IntAssemblyCategory,
    StaAssemblyCategory,
)


class AbstractAssembly(OdooObjectType):
    name = graphene.String(required=True)

    def resolve_assembly_category(root, info):
        return root.assembly_category_id or None

    def resolve_instance(root, info):
        return root.instance_id or None


class IntAssembly(AbstractAssembly):
    assembly_category = graphene.Field(IntAssemblyCategory)
    instance = graphene.Field(lambda: instance.IntInstance)


class ExtAssembly(AbstractAssembly):
    assembly_category = graphene.Field(ExtAssemblyCategory)
    instance = graphene.Field(lambda: instance.IntInstance)


class StaAssembly(AbstractAssembly):
    assembly_category = graphene.Field(StaAssemblyCategory)
    instance = graphene.Field(lambda: instance.StaInstance)
