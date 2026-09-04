# -*- coding: utf-8 -*-
{
    'name': 'Cupama Sales Customizations',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Price control, activity log, payment/order link and additional deliveries',
    'description': """
        Sales customizations for Cupama:
          - unit price and discount restricted to an authorized group (quotations and POS);
          - log notes when a product is created and when a quotation is created or updated;
          - customer payments linked to their sales order, which is locked once paid;
          - additional deliveries created from a sales order so the extra quantity
            can be invoiced on the same order.
    """,
    'author': 'A.Maximilien',
    'depends': ['sale_management', 'sale_stock'],
    'data': [
        'security/cupama_sale_groups.xml',
        'security/ir.model.access.csv',
        'wizard/sale_additional_delivery_views.xml',
        'views/sale_order_views.xml',
        'views/account_payment_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
