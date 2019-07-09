# Copyright 2016 Ilyas <https://github.com/ilyasProgrammer>
# Copyright 2016-2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2017-2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': """Pickup and pay at store""",
    'summary': """Simplify checkout process by excluding shipping and/or payment information""",
    'category': 'eCommerce',
    'images': ['images/1.png'],
    'version': '12.0.1.0.5',

    'author': 'IT-Projects LLC',
    "support": "apps@it-projects.info",
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
        'data/data.xml',
    ],
    "installable": True,
    'auto_install': False,
}
