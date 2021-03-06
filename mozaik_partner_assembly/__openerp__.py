# -*- coding: utf-8 -*-
##############################################################################
#
#     This file is part of mozaik_partner_assembly, an Odoo module.
#
#     Copyright (c) 2015 ACSONE SA/NV (<http://acsone.eu>)
#
#     mozaik_partner_assembly is free software:
#     you can redistribute it and/or
#     modify it under the terms of the GNU Affero General Public License
#     as published by the Free Software Foundation, either version 3 of
#     the License, or (at your option) any later version.
#
#     mozaik_partner_assembly is distributed in the hope that it will
#     be useful but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the
#     GNU Affero General Public License
#     along with mozaik_partner_assembly.
#     If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'MOZAIK: Partner - Assembly',
    'version': '1.0',
    "author": "ACSONE SA/NV",
    "maintainer": "ACSONE SA/NV",
    "website": "http://www.acsone.eu",
    'category': 'Political Association',
    'depends': [
        'mozaik_base',
    ],
    'description': """
MOZAIK Partner - Assembly
=========================
Add a readonly field 'is_assembly' to a partner.
This module is a dependency of both persons and structures modules.
""",
    'images': [
    ],
    'data': [
    ],
    'qweb': [
    ],
    'demo': [
    ],
    'test': [
    ],
    'license': 'AGPL-3',
    'sequence': 150,
    'auto_install': False,
    'installable': True,
}
