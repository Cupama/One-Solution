# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

#: identifier fields that must stay unique: field -> label shown to the user
UNIQUE_IDENTIFIERS = {
    'vat': 'VAT Num',
    'company_registry': 'BRN',
    'cupama_id_num': 'ID Num',
}


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # #1 WhatsApp number, displayed before the phone
    whatsapp_number = fields.Char(string='WhatsApp Number')

    # #2 / #3 relabel the native identifiers (attributes not given here are
    # kept from the base definition)
    company_registry = fields.Char(string='BRN')
    vat = fields.Char(string='VAT Num')

    # #6 identity card number for individuals
    cupama_id_num = fields.Char(string='ID Num', index='btree_not_null')

    # #4 / #5 / #6 duplicates are refused with an explicit message
    @api.constrains('vat', 'company_registry', 'cupama_id_num')
    def _check_unique_identifiers(self):
        for partner in self:
            for fname, label in UNIQUE_IDENTIFIERS.items():
                value = (partner[fname] or '').strip()
                if not value:
                    continue
                duplicate = self.with_context(active_test=False).sudo().search(
                    [
                        (fname, '=ilike', value),
                        ('id', '!=', partner.id),
                        # contacts of the same company share these values
                        ('commercial_partner_id', '!=',
                         partner.commercial_partner_id.id),
                        ('company_id', 'in', [False, partner.company_id.id]),
                    ],
                    limit=1,
                )
                if duplicate:
                    raise ValidationError(_(
                        'The %(label)s "%(value)s" is already used by the '
                        'contact "%(partner)s". It must be unique.',
                        label=label, value=value,
                        partner=duplicate.display_name,
                    ))
