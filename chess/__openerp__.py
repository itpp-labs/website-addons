# -*- coding: utf-8 -*-
{
    'name': "Chess",
    'summary': """Chess is online game""",
    'author': "IT-Projects LLC, Dinar Gabbasov",
    'website': "https://twitter.com/gabbasov_dinar",
    'category': 'Uncategorized',
    'version': '1.0.0',
    'depends': ['base', 'website', 'bus'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/chess_views.xml',
        'views/chess_templates.xml',
    ],
    'application': True,
}
