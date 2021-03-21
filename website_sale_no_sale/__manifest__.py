# Copyright 2018 Denis Mudarisov <https://it-projects.info/team/trojikman>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Stop Online Sales""",
    "summary": """Adds options to disable all sales and hide all prices, but keep products visible at website""",
    "category": "eCommerce",
    "images": ["images/main.jpg"],
    "version": "11.0.1.0.0",
    "application": False,
    "author": "IT-Projects LLC, Denis Mudarisov",
    "support": "apps@itpp.dev",
    "website": "https://itpp.dev",
    "license": "Other OSI approved licence",  # MIT
    "price": 45.00,
    "currency": "EUR",
    "depends": ["website_sale"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["templates.xml"],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
