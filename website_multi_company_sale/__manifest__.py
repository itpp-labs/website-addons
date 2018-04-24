# -*- coding: utf-8 -*-
{
    "name": """Real Multi Website (eCommerce extension)""",
    "summary": """Multi Website support in eCommerce""",
    "category": "eCommerce",
    "live_test_url": "http://apps.it-projects.info/shop/product/website-multi-company?version=11.0",
    "images": ["images/website_multi_company_sale_main.png"],
    "version": "11.0.1.2.0",
    "application": False,

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info/team/yelizariev",
    "license": "LGPL-3",
    "price": 9.00,
    "currency": "EUR",

    "depends": [
        "website_multi_company",
        "website_sale",
        "ir_rule_website",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/product_public_category_views.xml",
        "views/website_views.xml",
        "views/product_template_views.xml",
        "views/payment_views.xml",
        "security/website_multi_company_sale_security.xml",
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
