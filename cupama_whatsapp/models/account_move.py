# -*- coding: utf-8 -*-
from odoo import _, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_open_whatsapp(self):
        self.ensure_one()
        message = _(
            "Hello %(customer)s, your invoice %(ref)s of %(amount)s is available. "
            "Amount due: %(due)s.",
            customer=self.partner_id.name,
            ref=self.name or self.payment_reference or '',
            amount=self.currency_id.format(self.amount_total),
            due=self.currency_id.format(self.amount_residual),
        )
        return self.partner_id._whatsapp_action(message)
