# -*- coding: utf-8 -*-
{
    "name": """Real Multi Website""",
    "summary": """Yes, you can set up multi-company, multi-website, multi-eCommerce on a single database!""",
    "category": "eCommerce",
    # "live_test_URL": "",
    "images": ['images/website_multi_company_main.png'],
    "version": "1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@it-projects.info",
    "website": "https://twitter.com/yelizariev",
    "license": "LGPL-3",
    "price": 400.00,
    "currency": "EUR",

    "depends": [
        "website",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/website_views.xml",
        "views/website_templates.xml",
        "views/website_menu_views.xml",
        "views/res_config_views.xml",
    ],
    "qweb": [
    ],
    "demo": [
        # "data/website_demo.xml",
    ],

    "post_load": "post_load",
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,
}
