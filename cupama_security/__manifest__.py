# -*- coding: utf-8 -*-
{
    'name': 'Cupama Security',
    'version': '19.0.1.0.0',
    'category': 'Hidden',
    'summary': 'Deletion of business records restricted to administrators',
    'description': """
        Request #9: remove delete access for all users except Admin.

        Deleting contacts, products, quotations, purchase orders, invoices,
        payments and transfers is only possible for members of the
        "Cupama / Can Delete Records" group (administrators by default).
        Editing documents (removing a line from a quotation, etc.) is not
        affected.
    """,
    'author': 'A.Maximilien',
    'depends': ['sale_management', 'purchase', 'stock', 'account'],
    'data': [
        'security/cupama_security_groups.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
