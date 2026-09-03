# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

from . import log_utils


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # -- #16 Customer payment linked to its sales order --------------------
    sale_order_ids = fields.Many2many(
        comodel_name='sale.order',
        relation='cupama_sale_order_payment_rel',
        column1='payment_id',
        column2='order_id',
        string='Sales Orders',
        copy=False,
        help="Sales orders paid by this payment. They are locked when the "
             "payment is confirmed.",
    )
    lock_sale_order = fields.Boolean(
        string='Lock Orders on Confirmation',
        default=True,
    )

    @api.onchange('partner_id')
    def _onchange_partner_id_cupama(self):
        """Only keep orders of the selected customer."""
        for payment in self:
            payment.sale_order_ids = payment.sale_order_ids.filtered(
                lambda o: not payment.partner_id
                or o.partner_id.commercial_partner_id
                == payment.partner_id.commercial_partner_id
            )

    def action_post(self):
        res = super().action_post()
        self._cupama_process_sale_orders()
        return res

    def _cupama_process_sale_orders(self):
        for payment in self:
            if payment.payment_type != 'inbound':
                continue
            orders = payment.sale_order_ids
            if not orders:
                continue
            for order in orders:
                order.message_post(body=log_utils.note(_(
                    "Payment %(payment)s of %(amount)s %(currency)s "
                    "registered by %(user)s.",
                    payment=payment.name or payment.display_name,
                    amount='{:.2f}'.format(payment.amount),
                    currency=payment.currency_id.name,
                    user=self.env.user.name,
                )))
            if payment.lock_sale_order:
                to_lock = orders.filtered(
                    lambda o: o.state == 'sale' and not o.locked)
                if to_lock:
                    to_lock.sudo().action_lock()
                    for order in to_lock:
                        order.message_post(body=log_utils.note(_(
                            "Order locked after payment %s.",
                            payment.name or payment.display_name,
                        )))
