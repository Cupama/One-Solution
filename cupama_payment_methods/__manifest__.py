# -*- coding: utf-8 -*-
{
    'name': 'Cupama Payment Methods',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Bank Transfer, Cash, Juice, Card and Cheque payment methods',
    'description': """
        Request #11: sets up the five payment methods used by Cupama,
        both in accounting (journals) and in the Point of Sale:

          1. Bank Transfer
          2. Cash
          3. Juice (MCB Juice)
          4. Card
          5. Cheque

        The setup is idempotent: existing journals and methods are reused,
        nothing is duplicated when the module is reinstalled or updated.
    """,
    'author': 'A.Maximilien',
    'depends': ['account', 'point_of_sale'],
    'post_init_hook': '_setup_payment_methods',
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
