# -*- coding: utf-8 -*-
{
    "name": "pos_printer",
    "version": "15.0.0.0",
    "category": "Projects",
    "depends" : ['base','point_of_sale'],
    "author": "Mediod Consulting",
    "price": 50.00,
    'currency': "USD",
    'summary': '',
    "website": "https://mediodconsulting.com/",
    "data": [
        'security/ir.model.access.csv',
        # 'reports/orderreceipt_inherit.xml',
        'views/res_partner_inherit.xml',
    ],
        'assets': {'point_of_sale.assets': [
                                        'print_posreceipt/static/src/css/pos_receipt.css',
                                        'print_posreceipt/static/src/js/**/*',
                                        'print_posreceipt/static/src/xml/**/*',
                                        ],
               },
    "auto_install": False,
    "installable": True,
    'license': 'OPL-1',
}