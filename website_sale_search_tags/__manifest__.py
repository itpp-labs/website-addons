# -*- coding: utf-8 -*-
{
    "name": "Website #tag searching",
    "summary": """Search website products by tags""",
    "category": "eCommerce",
    "version": "10.0.1.0.3",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev, Savoir-faire Linux, Eugene Molotov",
    "license": "Other OSI approved licence",  # MIT
    "support": "apps@itpp.dev",
    "website": "https://it-projects.info",
    "images": ["images/search.png"],
    "depends": ["website_sale", "product_tags"],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "auto_install": False,
    "installable": True,
    "data": ["views/tours.xml"],
}
