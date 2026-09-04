# -*- coding: utf-8 -*-
import logging

from odoo import Command

_logger = logging.getLogger(__name__)

#: (name, journal code, journal type)
PAYMENT_METHODS = [
    ('Bank Transfer', 'BKTRF', 'bank'),
    ('Cash', 'CSH', 'cash'),
    ('Juice', 'JUICE', 'bank'),
    ('Card', 'CARD', 'bank'),
    ('Cheque', 'CHQ', 'bank'),
]


def _get_or_create_journal(env, company, name, code, jtype):
    Journal = env['account.journal'].with_company(company)
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


def _get_or_create_pos_method(env, company, name, journal):
    Method = env['pos.payment.method'].with_company(company)
    method = Method.search([
        ('name', '=ilike', name),
        ('company_id', 'in', [company.id, False]),
    ], limit=1)
    if method:
        return method
    return Method.create({
        'name': name, 'journal_id': journal.id, 'company_id': company.id,
    })


def _setup_payment_methods(env):
    for company in env['res.company'].search([]):
        if not company.chart_template:
            _logger.warning(
                "Cupama payment methods: company %s has no chart of accounts, "
                "skipped.", company.name)
            continue
        methods = env['pos.payment.method']
        for name, code, jtype in PAYMENT_METHODS:
            journal = _get_or_create_journal(env, company, name, code, jtype)
            methods |= _get_or_create_pos_method(env, company, name, journal)
        configs = env['pos.config'].with_context(active_test=False).search(
            [('company_id', '=', company.id)])
        # a cash method cannot be shared between several POS: only the
        # bank-type methods are spread over every shop.
        shareable = methods.filtered(lambda m: m.journal_id.type != 'cash')
        if configs and shareable:
            configs.write({
                'payment_method_ids': [Command.link(m.id) for m in shareable],
            })
