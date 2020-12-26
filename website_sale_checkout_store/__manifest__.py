# -*- coding: utf-8 -*-
# Copyright 2016 Ilyas <https://github.com/ilyasProgrammer>
# Copyright 2016-2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2017-2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# Copyright 2019 Karamov Ilmir <https://it-projects.info/team/ilmir-k>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Pickup and pay at store""",
    "summary": """Simplify checkout process by excluding shipping and/or payment information""",
    "category": "eCommerce",
    "images": ["images/1.png"],
    "version": "10.0.1.0.5",
    "author": "IT-Projects LLC",
    "support": "apps@itpp.dev",
    "website": "https://it-projects.info",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["website_sale"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["templates.xml", "views.xml", "data/data.xml"],
    "installable": False,
    "auto_install": False,
}
