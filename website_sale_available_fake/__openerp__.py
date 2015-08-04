{
    'name': "Sale limited quantity of products and restrict sale of private products",
    'version': '1.0.0',
    'author': 'Ivan Yelizariev',
    'category': 'Custom',
    'website': 'https://yelizariev.github.io',
    'depends': ['website_sale_available'],
    'data': [
        'website_sale_available_fake_views.xml',
        'security/security.xml',
        ],
    'installable': True,
}
