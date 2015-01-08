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

from openerp.osv import orm, fields
from openerp.tools import SUPERUSER_ID


class change_main_phone(orm.TransientModel):

    _name = 'change.main.phone'
    _inherit = 'change.main.coordinate'
    _description = 'Change Main Phone Wizard'

    _columns = {
        'old_phone_id': fields.many2one(
            'phone.phone', 'Current Main Phone'),
        'phone_id': fields.many2one(
            'phone.phone', 'New Main Phone',
            required=True, ondelete='cascade'),
        'partner_id': fields.many2one(
            'res.partner', 'Partner', ondelete='cascade'),
    }

    def default_get(self, cr, uid, flds, context):
        res = super(change_main_phone, self).default_get(cr, uid, flds, context=context)
        ids = context.get('active_ids') \
            or (context.get('active_id') and [context.get('active_id')]) \
            or []
        if len(ids) == 1:
            res['partner_id'] = ids[0]
        if context.get('mode', False) == 'switch':
            coord = self.pool.get(context.get('target_model')).browse(cr, uid, context.get('target_id', False))
            res['phone_id'] = coord.phone_id.id
        return res

    def onchange_phone_id(self, cr, uid, ids, phone_id, partner_id, context=None):
        res = {}
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, SUPERUSER_ID, partner_id, context=context)
            phone = self.pool.get('phone.phone').browse(cr, SUPERUSER_ID, phone_id, context=context)
            if phone.type == 'fix':
                res['old_phone_id'] = partner.fix_coordinate_id.phone_id.id or False
            elif phone.type == 'fax':
                res['old_phone_id'] = partner.fax_coordinate_id.phone_id.id or False
            else:
                res['old_phone_id'] = partner.mobile_coordinate_id.phone_id.id or False
            res['change_allowed'] = not(phone_id == res['old_phone_id'])
        return {'value': res}
