# -*- coding: utf-8 -*-
{
    'name': "Sale limited quantity of products and restrict sale of private products",
    'version': '1.0.0',
    'author': 'IT-Projects LLC, Ivan Yelizariev',
    'license': 'LGPL-3',
    'category': 'eCommerce',
    "support": "apps@it-projects.info",
    'website': 'https://yelizariev.github.io',
    'depends': ['website_sale_available'],
    'data': [
        'website_sale_available_fake_views.xml',
        'security/security.xml',
    ],
    'installable': False,
}
