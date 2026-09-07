# -*- coding: utf-8 -*-
{
    'name': 'Cupama WhatsApp',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Click-to-chat WhatsApp buttons on contacts, quotations and invoices',
    'description': """
        Request #8, option A (click-to-chat): a WhatsApp button on the
        contact, the quotation and the customer invoice, opening wa.me
        with the customer number and a pre-filled message. The message
        is sent from the user's own WhatsApp; nothing is stored by Meta
        on Odoo's behalf and no Meta Business account is needed.
    """,
    'author': 'A.Maximilien',
    'depends': ['cupama_contact', 'sale_management'],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
