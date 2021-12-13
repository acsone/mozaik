# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# pylint: disable=no-self-argument
# flake8: noqa

import graphene

from odoo.addons.graphql_base import OdooObjectType

from .assembly import ExtAssembly, IntAssembly, StaAssembly
from .instance import IntInstance
from .legislature import Legislature
from .mandate_category import MandateCategory
from .partner import Partner
from .thesaurus_term import ThesaurusTerm


class AbstractMandate(OdooObjectType):
    partner = graphene.Field(Partner, required=True)
    mandate_category = graphene.Field(MandateCategory, required=True)
    start_date = graphene.DateTime(required=True)
    deadline_date = graphene.DateTime(required=True)
    end_date = graphene.DateTime()

    def resolve_partner(root, info):
        return root.partner_id

    def resolve_mandate_category(root, info):
        return root.mandate_category_id

    def resolve_competencies(root, info):
        return root.competencies_m2m_ids or None


class IntMandate(AbstractMandate):
    int_assembly = graphene.Field(IntAssembly, required=True)
    mandate_instance = graphene.Field(IntInstance)

    def resolve_int_assembly(root, info):
        return root.int_assembly_id or None

    def resolve_mandate_instance(root, info):
        return root.mandate_instance_id or None


int_mandates = graphene.List(
    graphene.NonNull(IntMandate),
    required=True,
    description="All internal mandates",
    limit=graphene.Int(),
    offset=graphene.Int(),
)


def resolve_int_mandates(info, limit=None, offset=0):
    domain = []
    res = info.context["env"]["int.mandate"].search(domain, limit=limit, offset=offset)
    return res


class ExtMandate(AbstractMandate):
    ext_assembly = graphene.Field(ExtAssembly, required=True)
    competencies = graphene.List(graphene.NonNull(ThesaurusTerm))

    def resolve_ext_assembly(root, info):
        return root.ext_assembly_id or None


ext_mandates = graphene.List(
    graphene.NonNull(ExtMandate),
    required=True,
    description="All external mandates",
    limit=graphene.Int(),
    offset=graphene.Int(),
)


def resolve_ext_mandates(info, limit=None, offset=0):
    domain = []
    res = info.context["env"]["ext.mandate"].search(domain, limit=limit, offset=offset)
    return res


class StaMandate(AbstractMandate):
    sta_assembly = graphene.Field(StaAssembly, required=True)
    legislature = graphene.Field(Legislature, required=True)
    competencies = graphene.List(graphene.NonNull(ThesaurusTerm))

    def resolve_sta_assembly(root, info):
        return root.sta_assembly_id or None

    def resolve_legislature(root, info):
        return root.legislature_id


sta_mandates = graphene.List(
    graphene.NonNull(StaMandate),
    required=True,
    description="All state mandates",
    limit=graphene.Int(),
    offset=graphene.Int(),
)


def resolve_sta_mandates(info, limit=None, offset=0):
    domain = []
    res = info.context["env"]["sta.mandate"].search(domain, limit=limit, offset=offset)
    return res
