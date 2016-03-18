# -*- coding: utf-8 -*-
{
     "name": """Web login background""",
     "summary": """Set your background for odoo login page""",
     "category": "Base",
     "images": [],
     "version": "1.0.1",

     "author": "IT-Projects LLC, Ildar Nasyrov",
     "website": "https://it-projects.info",
     "license": "GPL-3",
     #"price": 9.00,
     #"currency": "EUR",

     "depends": [
         "base",
     ],
     "external_dependencies": {"python": [], "bin": []},
     "data": [
        'templates.xml',
        'views/attachment.xml',
     ],
     "demo": [
     ],
     "installable": True,
     "auto_install": False,
 }