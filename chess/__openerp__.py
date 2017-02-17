# -*- coding: utf-8 -*-
{
    "name": """Chess""",
    "summary": """Play Chess with other users in Odoo!""",
    "category": "Website",
    "version": "1.0.0",

    "author": "IT-Projects LLC, Dinar Gabbasov",
    "support": "apps@it-projects.info",
    'website': "https://twitter.com/gabbasov_dinar",
    "license": "LGPL-3",

    "depends": [
        "base",
        "website",
        "bus",
        "web",
    ],
    "external_dependencies": {
    "python": [
                "chess", 
                "concurrent.futures"
    ], 
    "bin": []
    },
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/chess_views.xml",
        "views/chess_templates.xml",
    ],

    "installable": True,
}
