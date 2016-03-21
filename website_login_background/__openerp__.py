# -*- coding: utf-8 -*-
{
    "name": """Website login background""",
    "summary": """Set your background on odoo login screen while you got website module installed.""",
    "category": "Website",
    "images": [],
    "version": "1.0.1",

    "author": "IT-Projects LLC",
    "website": "https://it-projects.info",
    "license": "LGPL-3",
    "price": 25.00,
    "currency": "EUR",

    "depends": [
        "web_login_background",
        "website",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "templates.xml",
    ],
    "demo": [
    ],
    "installable": True,
    "auto_install": True,
}