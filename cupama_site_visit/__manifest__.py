# -*- coding: utf-8 -*-
{
    'name': 'Cupama Site Visit Sheet',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Site Visit Sheet for SPC Flooring Installation',
    'description': """
        Module to manage site visit sheets for SPC flooring installation.
        Accessible via a smart button on Sale Orders and Quotations.
    """,
    'author': 'A.Maximilien',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/site_visit_sheet_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
