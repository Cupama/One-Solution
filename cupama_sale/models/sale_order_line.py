# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare

from . import log_utils

PRICE_FIELDS = {
    'price_unit': 'Product Price',
    'discount': 'Discount',
}
LOGGED_LINE_FIELDS = (
    'product_id', 'name', 'product_uom_qty', 'product_uom_id', 'price_unit', 'discount',
)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    can_edit_price = fields.Boolean(
        string='Can Edit Price',
        compute='_compute_can_edit_price',
        help="Technical field used to make the unit price and the discount "
             "read-only for users without the price edition right.",
    )
    is_additional_delivery = fields.Boolean(
        string='Additional Delivery',
        copy=False,
        readonly=True,
        help="Line added afterwards through the Additional Delivery action.",
    )
    additional_delivery_ref_id = fields.Many2one(
        comodel_name='stock.reference',
        string='Additional Delivery Reference',
        copy=False,
        readonly=True,
        help="Forces the additional quantity into its own delivery order "
             "instead of merging it with the deliveries of the sales order.",
    )

    def _compute_can_edit_price(self):
        can_edit = self.env.user.has_group('cupama_sale.group_sale_edit_price')
        for line in self:
            line.can_edit_price = can_edit

    # -- #17 Additional delivery ------------------------------------------
    def _prepare_procurement_values(self):
        """Send additional lines to their own delivery order."""
        values = super()._prepare_procurement_values()
        if self.additional_delivery_ref_id:
            values['reference_ids'] = self.additional_delivery_ref_id
        return values

    # -- ORM overrides -----------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines._log_lines_added()
        return lines

    def write(self, vals):
        self._check_price_edition(vals)
        watched = [f for f in LOGGED_LINE_FIELDS if f in vals]
        before = {}
        if watched and not self._skip_line_log():
            before = {line.id: log_utils.snapshot(line, watched) for line in self}
        res = super().write(vals)
        for line in self:
            changes = log_utils.diff(line, before.get(line.id, {}))
            if changes:
                line.order_id.message_post(body=log_utils.note(
                    _("Line updated: %s", line.product_id.display_name or line.name),
                    changes,
                ))
        return res

    def unlink(self):
        if not self._skip_line_log():
            for line in self:
                if line.display_type or not line.order_id:
                    continue
                line.order_id.message_post(body=log_utils.note(_(
                    "Line removed: %(product)s (%(qty)s %(uom)s)",
                    product=line.product_id.display_name or line.name,
                    qty=line.product_uom_qty,
                    uom=line.product_uom_id.display_name,
                )))
        return super().unlink()

    # -- #14 Log notes -----------------------------------------------------
    def _skip_line_log(self):
        return self.env.context.get('cupama_no_line_log')

    def _log_lines_added(self):
        if self._skip_line_log():
            return
        for line in self:
            if line.display_type or not line.order_id:
                continue
            line.order_id.message_post(body=log_utils.note(_(
                "Line added: %(product)s (%(qty)s %(uom)s)",
                product=line.product_id.display_name or line.name,
                qty=line.product_uom_qty,
                uom=line.product_uom_id.display_name,
            )))

    # -- #10 Price edition restricted -------------------------------------
    def _check_price_edition(self, vals):
        """Block manual changes of the unit price and the discount.

        Recomputations coming from the pricelist are left untouched: they either
        go through the compute cache or carry the ``sale_write_from_compute``
        context key.
        """
        if self.env.su or self.env.context.get('sale_write_from_compute'):
            return
        changed = [f for f in PRICE_FIELDS if f in vals]
        if not changed:
            return
        if self.env.user.has_group('cupama_sale.group_sale_edit_price'):
            return
        for line in self:
            if line.is_downpayment:
                continue
            for fname in changed:
                digits = self.env['decimal.precision'].precision_get(PRICE_FIELDS[fname])
                if float_compare(vals[fname] or 0.0, line[fname] or 0.0, precision_digits=digits):
                    raise UserError(_(
                        'You are not allowed to change the %(field)s on "%(line)s".\n'
                        'Ask a user who has the "Sales: Edit Unit Price" right.',
                        field=log_utils.field_label(line, fname),
                        line=line.product_id.display_name or line.name,
                    ))
