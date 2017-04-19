# -*- coding: utf-8 -*-
{
    "name": """Website sale cache""",
    "summary": """Cache module for Website Sales""",
    "category": "Website",
    "version": "1.0.0",

    "author": "IT-Projects LLC, Artyom Losev",
    "support": "apps@it-projects.info",
    'website': "https://www.it-projects.info",
    "license": "LGPL-3",

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
