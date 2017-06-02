# -*- coding: utf-8 -*-
{
    "name": """Web login background""",
    "summary": """Get a random background at the login page""",
    "category": "Extra Tools",
    "images": ['images/login.png'],
    "version": "1.0.1",

    "author": "IT-Projects LLC, Ildar Nasyrov",
    "website": "https://it-projects.info",
    "license": "GPL-3",
    "price": 15.00,
    "currency": "EUR",

    "depends": [
        "base",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'templates.xml',
        'views/attachment.xml',
    ],
    "demo": [
        'demo/demo.xml',
    ],
    "installable": True,
    "auto_install": False,
}
