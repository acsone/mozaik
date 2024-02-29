# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class IrModel(models.Model):
    _inherit = ["ir.model"]

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        self_sudo = self.sudo()
        return super(IrModel, self_sudo).name_search(
            name=name, args=args, operator=operator, limit=limit
        )
