# -*- coding: utf-8 -*-
{
    'name': 'Cupama POS Price Lock',
    'version': '19.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Restrict POS price modifications to managers on every shop',
    'description': """
        Enforces "Restrict Price Modifications to Managers" on all existing
        and future Point of Sale configurations (request #10).
        Cashiers must ask a POS manager to change a price.
    """,
    'author': 'A.Maximilien',
    'depends': ['point_of_sale'],
    'post_init_hook': '_enable_price_restriction',
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
