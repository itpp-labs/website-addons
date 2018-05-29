{
    'name': "Website Search Product Tags",
    'summary': """Search website products by tags""",
    'category': 'eCommerce',
    'version': '11.0.1.0.1',
    'application': False,
    'author': 'IT-Projects LLC, Ivan Yelizariev, Savoir-faire Linux, '
              'Quartile Limited Tim Lai',
    'license': 'GPL-3',
    "support": "apps@it-projects.info",
    'website': 'https://twitter.com/yelizariev',
    'price': 30.0,
    'currency': 'EUR',
    'images': ['images/search.png'],
    'depends': ['website_sale', 'product_tags'],
    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,

    'auto_install': False,
    'installable': False,
}
