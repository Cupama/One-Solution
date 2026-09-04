# -*- coding: utf-8 -*-
from odoo import _, api, models

from . import log_utils

#: Product fields worth a log note (#14).
LOGGED_PRODUCT_FIELDS = (
    'name', 'default_code', 'barcode', 'categ_id', 'type', 'list_price',
    'standard_price', 'taxes_id', 'supplier_taxes_id', 'uom_id',
    'sale_ok', 'purchase_ok', 'active',
)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        for template in templates:
            items = [
                _("%(field)s: %(value)s",
                  field=log_utils.field_label(template, fname),
                  value=log_utils.field_value(template, fname))
                for fname in ('categ_id', 'type', 'list_price', 'standard_price')
            ]
            template.message_post(body=log_utils.note(
                _("Product created by %s.", self.env.user.name), items,
            ))
        return templates

    def write(self, vals):
        watched = [f for f in LOGGED_PRODUCT_FIELDS if f in vals]
        before = {
            template.id: log_utils.snapshot(template, watched)
            for template in self
        } if watched else {}
        res = super().write(vals)
        for template in self:
            changes = log_utils.diff(template, before.get(template.id, {}))
            if changes:
                template.message_post(body=log_utils.note(
                    _("Product updated by %s.", self.env.user.name), changes,
                ))
        return res
