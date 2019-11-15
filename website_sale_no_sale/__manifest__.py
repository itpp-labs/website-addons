# Copyright 2018 Denis Mudarisov <https://it-projects.info/team/trojikman>
# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """Stop Online Sales""",
    "summary": """Adds options to disable all sales and hide all prices, but keep products visible at website""",
    "category": "eCommerce",
    "images": ["images/main.jpg"],
    "version": "12.0.1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Denis Mudarisov",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info/team/trojikman",
    "license": "LGPL-3",
    "price": 45.00,
    "currency": "EUR",

    "depends": [
        "website_sale",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "templates.xml",
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": True,
}
