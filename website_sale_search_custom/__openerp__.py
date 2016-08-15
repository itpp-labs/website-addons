# -*- coding: utf-8 -*-
{
    'name': "Custom website search",
    'version': '1.0.0',
    'author': 'IT-Projects LLC, Ivan Yelizariev',
    'license': 'GPL-3',
    'category': 'eCommerce',
    'website': 'https://twitter.com/yelizariev',
    'price': 9.00,
    'currency': 'EUR',
    'images': ['images/search.png'],
    'depends': ['website_sale', 'product_tags'],
    'data': [
        'views.xml',
    ],
    "post_load": 'post_load',
    'installable': True
}
