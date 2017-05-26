# -*- coding: utf-8 -*-
{
    "name": """E-commerce Category Cache""",
    "summary": """Use this module to greatly accelerate the loading of a page with a large number of product categories""",
    "category": "Website",
    "images": ['images/websale_cache.png'],
    "version": "1.0.0",

    "author": "IT-Projects LLC, Artyom Losev",
    "support": "apps@it-projects.info",
    'website': "https://www.it-projects.info",
    "license": "LGPL-3",
    "price": 49.00,
    "currency": "EUR",

    "depends": [
        "website_sale",
        "website",
        "base_action_rule",
    ],
    "data": [
        "views.xml",
        "data/ir_action_server.xml",
        "data/base_action_rules.xml",
    ],
    "installable": True,
}
