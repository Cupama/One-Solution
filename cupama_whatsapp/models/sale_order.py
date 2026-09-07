# -*- coding: utf-8 -*-
from odoo import _, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_whatsapp(self):
        self.ensure_one()
        message = _(
            "Hello %(customer)s, your %(doc)s %(ref)s of %(amount)s is ready. "
            "Feel free to contact us for any question.",
            customer=self.partner_id.name,
            doc=_("order") if self.state == 'sale' else _("quotation"),
            ref=self.name,
            amount=self.currency_id.format(self.amount_total),
        )
        return self.partner_id._whatsapp_action(message)
