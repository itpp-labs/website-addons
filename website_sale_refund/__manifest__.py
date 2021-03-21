# -*- coding: utf-8 -*-
{
    "name": """Product swap at eCommerce""",
    "summary": """Product upgrading / changing feature for your online shop""",
    "category": "eCommerce",
    # "live_test_url": "",
    "images": ["images/banner.jpg"],
    "version": "10.0.1.0.1",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@itpp.dev",
    "website": "https://twitter.com/OdooFree",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["website_sale"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "data/product.xml",
        "views/website_sale_templates.xml",
        "views/sale_order_views.xml",
    ],
    "qweb": [],
    "demo": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
