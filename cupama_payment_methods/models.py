# -*- coding: utf-8 -*-
import logging

from odoo import Command, models

_logger = logging.getLogger(__name__)

#: (name, journal code, journal type)
PAYMENT_METHODS = [
    ('Bank Transfer', 'BKTRF', 'bank'),
    ('Cash', 'CSH', 'cash'),
    ('Juice', 'JUICE', 'bank'),
    ('Card', 'CARD', 'bank'),
    ('Cheque', 'CHQ', 'bank'),
]


class CupamaPaymentSetup(models.AbstractModel):
    _name = 'cupama.payment.setup'
    _description = 'Cupama Payment Methods Setup'

    def _get_or_create_journal(self, company, name, code, jtype):
        Journal = self.env['account.journal'].with_company(company)
        domain = [('company_id', '=', company.id)]
        journal = Journal.search(
            domain + ['|', ('name', '=ilike', name), ('code', '=', code)], limit=1)
        if journal:
            return journal
        if jtype == 'cash':
            # reuse the default cash journal instead of creating a second one
            journal = Journal.search(domain + [('type', '=', 'cash')], limit=1)
            if journal:
                return journal
        return Journal.create({
            'name': name, 'code': code, 'type': jtype, 'company_id': company.id,
        })

    def _get_or_create_pos_method(self, company, name, journal):
        Method = self.env['pos.payment.method'].with_company(company)
        method = Method.search([
            ('name', '=ilike', name),
            ('company_id', 'in', [company.id, False]),
        ], limit=1)
        if method:
            return method
        return Method.create({
            'name': name, 'journal_id': journal.id, 'company_id': company.id,
        })

    def run(self):
        """Create the journals/POS methods and link them to every shop.

        Executed on each install and update of the module (data <function/>),
        idempotent, so a shop skipped because its session was open is linked
        on the next update.
        """
        for company in self.env['res.company'].search([]):
            if not company.chart_template:
                _logger.warning(
                    "Cupama payment methods: company %s has no chart of "
                    "accounts, skipped.", company.name)
                continue
            methods = self.env['pos.payment.method']
            for name, code, jtype in PAYMENT_METHODS:
                journal = self._get_or_create_journal(company, name, code, jtype)
                methods |= self._get_or_create_pos_method(company, name, journal)
            configs = self.env['pos.config'].with_context(active_test=False).search(
                [('company_id', '=', company.id)])
            # Odoo refuses any change to the payment methods of a POS whose
            # session is still open: those shops are linked on the next
            # module update, once their session is closed.
            open_configs = configs.filtered('has_active_session')
            if open_configs:
                _logger.warning(
                    "Cupama payment methods: POS with an open session skipped: "
                    "%s. Close the session(s) and update the module to link "
                    "them.", ', '.join(open_configs.mapped('name')))
            configs -= open_configs
            # a cash method cannot be shared between several POS: only the
            # bank-type methods are spread over every shop.
            shareable = methods.filtered(lambda m: m.journal_id.type != 'cash')
            if configs and shareable:
                configs.write({
                    'payment_method_ids': [Command.link(m.id) for m in shareable],
                })
