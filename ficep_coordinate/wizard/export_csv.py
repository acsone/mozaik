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

import tempfile
import csv
from collections import OrderedDict

from openerp.tools.translate import _
from openerp.osv import orm

from openerp.addons.ficep_person.res_partner import available_genders, available_tongues

HEADER_ROW = [
    'Internal Identifier',
    'Name',
    'Lastname',
    'Firstname',
    'Usual Lastname',
    'Usual Firstname',
    'Co-Residency Line 1',
    'Co-Residency Line 2',
    'Main Address',
    'Unauthorized Address',
    'Vip Address',
    'Country Code',
    'Country Name',
    'Zip',
    'Street',
    'Street2',
    'City',
    'Internal Instance',
    'Reference',
    'Birthdate',
    'Gender',
    'Tongue',
    'Main Phone',
    'Unauthorized Phone',
    'Vip Phone',
    'Phone',
    'Main Mobile',
    'Unauthorized Mobile',
    'Vip Mobile',
    'Mobile',
    'Main Fax',
    'Unauthorized Fax',
    'Vip Fax',
    'Fax',
    'Main Email',
    'Unauthorized Email',
    'Vip Email',
    'Email',
]


class export_csv(orm.TransientModel):
    _name = 'export.csv'
    _description = 'Export CSV Wizard'

    _columns = {
    }

    def get_csv_rows(self, cr, uid, model, context=None):
        """
        =============
        get_csv_rows
        =============
        Get the rows (header) for the specified model.
        """
        return HEADER_ROW

    def get_csv_values(self, cr, uid, model, obj, context=None):
        """
        ==============
        get_csv_values
        ==============
        Get the values of the specified obj, which should be an instance
        of the specified model, either an email or a postal coordinate.
        """

        def safe_get(o, attr, default=None):
            try:
                return getattr(o, attr)
            except orm.except_orm:
                return default

        def _get_utf8(data):
            if not data:
                return None
            return data.encode('utf-8')

        # Test access coordinate (VIP READER)
        partner = safe_get(obj, 'partner_id')

        if not partner:
            return False

        if model == 'postal.coordinate':
            # for postal coordinates, get email coordinate from the partner
            pc = obj
            ec = partner.email_coordinate_id or None
        elif model == 'email.coordinate':
            # for email coordinates, get postal coordinate from the partner
            ec = obj
            pc = partner.postal_coordinate_id or None

        xc = partner.fix_coordinate_id or None
        mc = partner.mobile_coordinate_id or None
        fc = partner.fax_coordinate_id or None

        cc = pc and pc.co_residency_id
        ic = partner.int_instance_id

        export_values = OrderedDict([
            ('identifier', partner.identifier or None),
             ('name', _get_utf8(partner.name)),
             ('lastname', _get_utf8(partner.lastname)),
             ('firstname', _get_utf8(partner.firstname)),
             ('usual_lastname', _get_utf8(partner.usual_lastname)),
             ('usual_firstname', _get_utf8(partner.usual_firstname)),
             ('printable_name', cc and _get_utf8(cc.line) or
                                _get_utf8(partner.printable_name)),
             ('co_residency', cc and _get_utf8(cc.line2)),
             ('adr_main', pc and pc.is_main or False),
             ('adr_unauthorized', pc and pc.unauthorized or False),
             ('adr_vip', pc and pc.vip or False),
             ('country_code', pc and pc.address_id.country_code),
             ('country_name', pc and _get_utf8(pc.address_id.country_id.name)),
             ('zip', pc and pc.address_id.zip),
             ('street', pc and _get_utf8(pc.address_id.street)),
             ('street2', pc and _get_utf8(pc.address_id.street2)),
             ('city', pc and _get_utf8(pc.address_id.city)),
             ('instance', ic and _get_utf8(ic.name)),
             ('reference', _get_utf8(partner.reference)),
             ('birth_date', partner.birth_date or None),
             ('gender', available_genders.get(partner.gender, None)),
             ('tongue', available_tongues.get(partner.tongue, None)),
             ('fix_main', xc and xc.is_main or False),
             ('fix_unauthorized', xc and xc.unauthorized or False),
             ('fix_vip', xc and xc.vip or False),
             ('fix', xc and _get_utf8(xc.phone_id.name)),
             ('mobile_main', mc and mc.is_main or False),
             ('mobile_unauthorized', mc and mc.unauthorized or False),
             ('mobile_vip', mc and mc.vip or False),
             ('mobile', mc and _get_utf8(mc.phone_id.name)),
             ('fax_main', fc and fc.is_main or False),
             ('fax_unauthorized', fc and fc.unauthorized or False),
             ('fax_vip', fc and fc.vip or False),
             ('fax', fc and _get_utf8(fc.phone_id.name)),
             ('email_main', ec and ec.is_main or False),
             ('email_unauthorized', ec and ec.unauthorized or False),
             ('email_vip', ec and ec.vip or False),
             ('email', ec and _get_utf8(ec.email)),
        ])
        return export_values

    def get_csv(self, cr, uid, model, model_ids, group_by=False, context=None):
        """
        ========
        get_csv
        ========
        Get a CSV file with data of postal_ids depending of ``HEADER_ROW``
        """

        if model not in ['postal.coordinate', 'email.coordinate']:
            return

        objects = self.pool[model].browse(cr, uid, model_ids, context=context)
        tmp = tempfile.NamedTemporaryFile(prefix='Extract', suffix=".csv",
                                          delete=False)
        f = open(tmp.name, "r+")
        writer = csv.writer(f)
        writer.writerow(self.get_csv_rows(cr, uid, model, context=context))
        co_residencies = []
        for obj in objects:
            if model == 'postal.coordinate':
                # when grouping by co_residency, output only one row
                # by co_residency
                if group_by and obj.co_residency_id and \
                   obj.co_residency_id.id in co_residencies:
                    continue
                co_residencies.append(obj.co_residency_id.id)

            export_values = self.get_csv_values(cr, uid, model, obj)
            if not export_values:
                continue

            writer.writerow(export_values.values())
        f.close()
        f = open(tmp.name, "r")
        csv_content = f.read()
        f.close()
        return csv_content

    def export(self, cr, uid, ids, context=None):
        model = context.get('active_model', False)
        model_ids = context.get('active_ids', False)
        csv_content = self.get_csv(cr, uid, model, model_ids, context=context)

        # Send to current user
        attachment = [(_('Extract.csv'), '%s' % csv_content)]
        partner_ids = self.pool['res.partner'].search(
            cr, uid, [('user_ids', '=', uid)], context=context)
        if partner_ids:
            self.pool['mail.thread'].message_post(cr, uid,
                False, attachments=attachment, context=context,
                partner_ids=partner_ids, subject=_('Export CSV'))
        return True
