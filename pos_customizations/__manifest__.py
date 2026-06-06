# -*- coding: utf-8 -*-
{
    'name': "POS Customizations",
    'summary': """Log in to configured POS shop to save time without backend.""",
    'description': """
        Log in to configured POS shop to save time without backend.
    """,
    'author': "Ali Hassan",
    'category': 'pos',
    'version': '19.0.1.0.0',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'data/res_groups.xml',
        'views/res_users_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_customizations/static/src/js/**/*.js',
            'pos_customizations/static/src/xml/**/*.xml',
        ],
    },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
