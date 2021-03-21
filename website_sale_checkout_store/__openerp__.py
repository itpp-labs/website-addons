# -*- coding: utf-8 -*-
{
    'name': """Pickup and pay at store""",
    'summary': """Simplify checkout process by excluding shipping and/or payment information""",
    'category': 'eCommerce',
    'images': ['images/1.png'],
    'version': '1.0.0',

    'author': 'IT-Projects LLC',
    'website': 'https://twitter.com/OdooFree',
    'license': 'LGPL-3',

    'depends': [
        'website_sale',
    ],
    'external_dependencies': {'python': [], 'bin': []},
    'data': [
        'templates.xml',
        'views.xml',
        'data/data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
