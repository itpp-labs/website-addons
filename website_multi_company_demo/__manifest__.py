# -*- coding: utf-8 -*-
{
    "name": """Demo Data for \"Real Multi Website\"""",
    "summary": """Provides demo websites""",
    "category": "eCommerce",
    # "live_test_URL": "",
    "images": [],
    "version": "1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info",
    "license": "LGPL-3",
    # "price": 9.00,
    # "currency": "EUR",

    "depends": [
        "website_multi_company",
        "website_sale",
        "theme_bootswatch",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
    ],
    "qweb": [
    ],
    "demo": [
        "demo/res.company.csv",
        "demo/website.csv",
        "demo/product.template.csv",
        "demo/ir.ui.view.csv",
        "demo/website.menu.csv",
        "demo/website_templates.xml",
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,
}
