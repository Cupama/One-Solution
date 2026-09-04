# -*- coding: utf-8 -*-
from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError

from ..models import log_utils


class SaleAdditionalDelivery(models.TransientModel):
    _name = 'cupama.sale.additional.delivery'
    _description = 'Create an Additional Delivery on a Sales Order'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sales Order',
        required=True,
        readonly=True,
    )
    partner_id = fields.Many2one(
        related='sale_order_id.partner_id', string='Customer')
    reason = fields.Char(
        string='Reason',
        required=True,
        help="Why this extra quantity is delivered (logged on the order).",
    )
    line_ids = fields.One2many(
        comodel_name='cupama.sale.additional.delivery.line',
        inverse_name='wizard_id',
        string='Products',
    )

    def action_confirm(self):
        self.ensure_one()
        order = self.sale_order_id
        if order.state != 'sale':
            raise UserError(_(
                "An additional delivery can only be created on a confirmed "
                "sales order."))
        lines = self.line_ids.filtered(lambda l: l.quantity > 0)
        if not lines:
            raise UserError(_("Add at least one product with a quantity."))

        reference = self.env['stock.reference'].create({
            'name': _("%s - Additional", order.name),
            'sale_ids': [Command.link(order.id)],
        })

        # Adding a line on a confirmed order launches the stock rule, and the
        # dedicated stock.reference keeps the move out of the existing
        # deliveries (see sale.order.line._prepare_procurement_values).
        was_locked = order.locked
        if was_locked:
            order.sudo().action_unlock()
        try:
            so_lines = self.env['sale.order.line'].with_context(
                cupama_no_line_log=True,
            ).create([line._prepare_order_line_values(reference) for line in lines])
        finally:
            if was_locked:
                order.sudo().action_lock()

        pickings = so_lines.move_ids.picking_id
        pickings.write({
            'is_additional_delivery': True,
            'additional_delivery_reason': self.reason,
        })

        order.message_post(body=log_utils.note(
            _("Additional delivery %(pickings)s created by %(user)s (%(reason)s).",
              pickings=', '.join(pickings.mapped('name')) or _("(no stock move)"),
              user=self.env.user.name,
              reason=self.reason),
            [
                _("%(qty)s x %(product)s",
                  qty=line.quantity, product=line.product_id.display_name)
                for line in lines
            ],
        ))

        if not pickings:
            return {'type': 'ir.actions.act_window_close'}
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Additional Delivery'),
            'res_model': 'stock.picking',
            'view_mode': 'list,form',
            'domain': [('id', 'in', pickings.ids)],
        }
        if len(pickings) == 1:
            action.update(view_mode='form', res_id=pickings.id)
        return action


class SaleAdditionalDeliveryLine(models.TransientModel):
    _name = 'cupama.sale.additional.delivery.line'
    _description = 'Additional Delivery Line'

    wizard_id = fields.Many2one(
        comodel_name='cupama.sale.additional.delivery',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
        domain=[('type', '=', 'consu')],
    )
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    price_unit = fields.Float(
        string='Unit Price',
        compute='_compute_price_unit',
        store=True,
        readonly=False,
        help="Price invoiced for the additional quantity. Defaults to the "
             "pricelist price of the order.",
    )
    can_edit_price = fields.Boolean(compute='_compute_can_edit_price')

    @api.depends('product_id', 'quantity')
    def _compute_price_unit(self):
        for line in self:
            order = line.wizard_id.sale_order_id
            if not line.product_id:
                line.price_unit = 0.0
            elif order.pricelist_id:
                line.price_unit = order.pricelist_id._get_product_price(
                    line.product_id,
                    line.quantity or 1.0,
                    currency=order.currency_id,
                    date=order.date_order,
                )
            else:
                line.price_unit = line.product_id.list_price

    def _compute_can_edit_price(self):
        can_edit = self.env.user.has_group('cupama_sale.group_sale_edit_price')
        for line in self:
            line.can_edit_price = can_edit

    def _prepare_order_line_values(self, reference):
        self.ensure_one()
        return {
            'order_id': self.wizard_id.sale_order_id.id,
            'product_id': self.product_id.id,
            'product_uom_qty': self.quantity,
            'price_unit': self.price_unit,
            'is_additional_delivery': True,
            'additional_delivery_ref_id': reference.id,
        }
