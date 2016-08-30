# -*- coding: utf-8 -*-
{
    'name': """Pickup and pay at store""",
    'summary': """Simplify checkout process by excluding shipping and/or payment information""",
    'category': 'eCommerce',
    'images': ['images/1.png'],
    'version': '1.0.0',

    'author': 'IT-Projects LLC',
    'website': 'https://it-projects.info',
    'license': 'LGPL-3',
    'price': 90.00,
    'currency': 'EUR',

    'depends': [
        'website_sale',
    ],
    'external_dependencies': {'python': [], 'bin': []},
    'data': [
        'templates.xml',
        'views.xml',
    ],
    'demo': [
        'demo/demo.xml'
    ],
    'installable': False,
    'auto_install': False,
}
