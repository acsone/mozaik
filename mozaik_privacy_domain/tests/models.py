# Copyright 2024 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models


class ResCountryWithPrivacyDomain(models.Model):
    _inherit = ["res.country", "privacy.domain.mixin"]
    _description = "Adding privacy domain on countries"
