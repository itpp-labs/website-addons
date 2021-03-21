# -*- coding: utf-8 -*-
{
    "name": """Web login background""",
    "summary": """Get a random background at the login page""",
    "category": "Extra Tools",
    "images": ['images/login.png'],
    "version": "1.0.1",

    "author": "IT-Projects LLC, Ildar Nasyrov",
    "website": "https://twitter.com/OdooFree",
    "license": "LGPL-3",

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
