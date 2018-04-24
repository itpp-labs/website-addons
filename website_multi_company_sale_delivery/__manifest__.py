# -*- coding: utf-8 -*-
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """Real Multi Website (eCommerce Delivery extension)""",
    "summary": """Configure Delivery Carriers list per website""",
    "category": "eCommerce",
    "live_test_url": "http://apps.it-projects.info/shop/product/website-multi-company?version=11.0",
    "images": [],
    "version": "11.0.1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Ildar Nasyrov",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info/team/iledarn",
    "license": "LGPL-3",
    "price": 19.00,
    "currency": "EUR",

    "depends": [
        "website_sale_delivery",
        "ir_rule_website",
        "website_multi_company",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/website_multi_company_sale_delivery_security.xml",
        "security/ir.model.access.csv",
        "views/delivery_views.xml",
    ],
    "qweb": [
    ],
    "demo": [
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": True,
}
