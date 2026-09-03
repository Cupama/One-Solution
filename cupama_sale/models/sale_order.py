# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

from . import log_utils

#: Header fields worth a log note (#14). state / partner_id are already
#: tracked natively by Odoo.
LOGGED_ORDER_FIELDS = (
    'partner_invoice_id', 'partner_shipping_id', 'validity_date',
    'commitment_date', 'pricelist_id', 'payment_term_id', 'client_order_ref',
)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # -- #16 Customer payments linked to the order -------------------------
    payment_ids = fields.Many2many(
        comodel_name='account.payment',
        relation='cupama_sale_order_payment_rel',
        column1='order_id',
        column2='payment_id',
        string='Customer Payments',
        copy=False,
    )
    payment_count = fields.Integer(compute='_compute_payment_amounts')
    amount_paid_direct = fields.Monetary(
        string='Payments Received',
        compute='_compute_payment_amounts',
        help="Total of the posted customer payments linked to this order.",
    )

    @api.depends('payment_ids', 'payment_ids.state', 'payment_ids.amount')
    def _compute_payment_amounts(self):
        for order in self:
            posted = order.payment_ids.filtered(
                lambda p: p.state in ('in_process', 'paid')
                and p.payment_type == 'inbound'
            )
            order.payment_count = len(order.payment_ids)
            order.amount_paid_direct = sum(
                p.currency_id._convert(
                    p.amount, order.currency_id, order.company_id,
                    p.date or fields.Date.context_today(order),
                ) for p in posted
            )

    def action_view_payments(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Customer Payments'),
            'res_model': 'account.payment',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.payment_ids.ids)],
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_payment_type': 'inbound',
                'default_partner_type': 'customer',
                'default_sale_order_ids': [(4, self.id)],
            },
        }
        if len(self.payment_ids) == 1:
            action.update(view_mode='form', res_id=self.payment_ids.id)
        return action

    # -- #17 Additional deliveries -----------------------------------------
    additional_delivery_count = fields.Integer(
        compute='_compute_additional_delivery_count',
    )

    @api.depends('picking_ids.is_additional_delivery')
    def _compute_additional_delivery_count(self):
        for order in self:
            order.additional_delivery_count = len(
                order.picking_ids.filtered('is_additional_delivery')
            )

    def action_open_additional_delivery_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Additional Delivery'),
            'res_model': 'cupama.sale.additional.delivery',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_order_id': self.id},
        }

    # -- #14 Log notes ------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        # the creation note below already lists the initial lines
        orders = super(
            SaleOrder, self.with_context(cupama_no_line_log=True)
        ).create(vals_list).with_env(self.env)
        for order in orders:
            items = [
                _("%(qty)s x %(product)s",
                  qty=line.product_uom_qty,
                  product=line.product_id.display_name or line.name)
                for line in order.order_line if not line.display_type
            ]
            order.message_post(body=log_utils.note(
                _("Quotation created by %s.", self.env.user.name), items,
            ))
        return orders

    def write(self, vals):
        watched = [f for f in LOGGED_ORDER_FIELDS if f in vals]
        before = {
            order.id: log_utils.snapshot(order, watched) for order in self
        } if watched else {}
        res = super().write(vals)
        for order in self:
            changes = log_utils.diff(order, before.get(order.id, {}))
            if changes:
                order.message_post(body=log_utils.note(
                    _("Quotation updated by %s.", self.env.user.name), changes,
                ))
        return res
