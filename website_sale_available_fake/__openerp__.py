{
    'name': "Sale limited quantity of products and restrict sale of private products",
    'version': '1.0.0',
    'author': 'IT-Projects LLC, Ivan Yelizariev',
    'license': 'GPL-3',
    'category': 'Custom',
    'website': 'https://yelizariev.github.io',
    'depends': ['website_sale_available'],
    'data': [
        'website_sale_available_fake_views.xml',
        'security/security.xml',
        ],
    'installable': True,
}
