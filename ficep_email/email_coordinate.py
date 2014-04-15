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
import re

from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp.tools.mail import single_email_re


class email_coordinate(orm.Model):

    _name = 'email.coordinate'
    _inherit = ['abstract.coordinate']
    _description = "Email Coordinate"

    _discriminant_field = 'email'
    _undo_redirect_action = 'ficep_email.email_coordinate_action'

    _columns = {
        'name': fields.related('partner_id', 'printable_name', string='Partner Name', type='char',
                               relation='res.partner'),
        'email': fields.char('Email', size=100, required=True, select=True),
    }

    _rec_name = _discriminant_field

    def _check_email(self, cr, uid, ids, context=None):
        coordinates = self.browse(cr, uid, ids, context=context)
        for coordinate in coordinates:
            if not re.match(single_email_re, coordinate.email) != None:
                return False
        return True

    _constraints = [
        (_check_email, _('Invalid Email Format'), ['email']),
    ]

#orm methods

    def create(self, cr, uid, vals, context=None):
        """
        ======
        create
        ======
        format email by removing whitespace and changing upper to lower
        """
        if 'email' in vals:
            vals['email'] = self.format_email(cr, uid, vals['email'], context=context)
        return super(email_coordinate, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        """
        =====
        write
        =====
        format email by removing whitespace and changing upper to lower
        """
        if 'email' in vals:
            vals['email'] = self.format_email(cr, uid, vals['email'], context=context)
        return super(email_coordinate, self).write(cr, uid, ids, vals, context=context)

    def format_email(self, cr, uid, value, context=None):
        """
        ============
        format_email
        ============
        :type value: char
        :rtype: char
        :rparam value: value without space and in lower case
        """
        value = value.lower().strip()
        value = value.replace(' ', '')
        return value
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
