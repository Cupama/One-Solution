# -*- coding: utf-8 -*-

{
    'name': 'Inter Company Sale Purchase',
    'category': 'Inter Company Sale',
    'summary': 'Sale and Purchase',
    'author': 'Team Alpha',
    'depends': ['sale_management', 'purchase'],
    'data': [
        'views/purchase_order_ext.xml',
    ],
    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
