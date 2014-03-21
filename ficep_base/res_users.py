# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2014 Acsone SA/NV (http://www.acsone.eu)
#    All Rights Reserved
#
#    WARNING: This program as such is intended to be used by professional
#    programmers who take the whole responsibility of assessing all potential
#    consequences resulting from its eventual inadequacies and bugs.
#    End users who are looking for a ready-to-use solution with commercial
#    guarantees and support are strongly advised to contact a Free Software
#    Service Company.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm
from openerp import tools
from openerp.tools import SUPERUSER_ID


class res_users(orm.Model):

    _inherit = 'res.users'

    _defaults = {
        'groups_id': False,
        'display_groups_suggestions': False,
    }

# overriden model methods

    @tools.ormcache(skiparg=2)
    def context_get(self, cr, uid, context=None):
        result = super(res_users, self).context_get(cr, uid)
        user = self.browse(cr, SUPERUSER_ID, uid, context)
        _, appl_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'base', 'module_category_political_association')
        for g in user.groups_id:
            if g.category_id.id == appl_id:
                result.update({'in_%s' % g.name.lower().replace(' ', '_'): 1})
        return result

    def write(self, cr, uid, ids, vals, context=None):
        res = super(res_users, self).write(cr, uid, ids, vals, context=context)
        super(res_users, self).context_get.clear_cache(self)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
