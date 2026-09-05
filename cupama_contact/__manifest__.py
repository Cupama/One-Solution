# -*- coding: utf-8 -*-
{
    'name': 'Cupama Contacts',
    'version': '19.0.1.0.5',
    'category': 'Contacts',
    'summary': 'WhatsApp number, BRN / VAT Num / ID Num with duplicate control',
    'description': """
        Contact customizations for Cupama:
          - "WhatsApp Number" field before the phone (request #1);
          - "Company I.D" relabelled "BRN" (request #2);
          - "Tax I.D" relabelled "VAT Num" (request #3);
          - BRN and VAT Num must be unique, duplicates are refused with a
            clear message (requests #4 and #5);
          - "ID Num" field for individuals, unique as well (request #6).
    """,
    'author': 'A.Maximilien',
    'depends': ['base', 'contacts'],
    'data': [
        'data/res_country_data.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
