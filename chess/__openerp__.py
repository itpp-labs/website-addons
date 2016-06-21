# -*- coding: utf-8 -*-
{
    "name": """Chess""",
    "summary": """Play Chess with other users in Odoo!""",
    "category": "Website",
    "version": "1.0.0",

    "author": "IT-Projects LLC, Dinar Gabbasov",
    'website': "https://twitter.com/gabbasov_dinar",
    "license": "GPL-3",

    "depends": [
        "base",
        "website",
        "bus",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/chess_views.xml",
        "views/chess_templates.xml",
    ],

    "installable": True,
}
