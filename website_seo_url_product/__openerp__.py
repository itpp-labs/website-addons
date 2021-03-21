# -*- coding: utf-8 -*-
{
    "name": """SEO URLs in eCommerce""",
    "summary": """Customisable URLs for product pages, that don't depend on product name and product ID""",
    "category": "eCommerce",
    "images": [],
    "version": "1.0.0",

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "website": "https://twitter.com/OdooFree",
    "license": "LGPL-3",

    "depends": [
        "website_seo_url",
        "product",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views.xml",
    ],
    "qweb": [
    ],
    "demo": [
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": True,
    "auto_install": False,
}
