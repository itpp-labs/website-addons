# -*- coding: utf-8 -*-
{
    "name": """Autopay in eCommerce""",
    "summary": """Auto invoice creating on payment""",
    "category": "eCommerce",
    "images": [],
    "version": "1.0.0",

    "author": "IT-Projects LLC",
    "website": "https://it-projects.info",
    "license": "LGPL-3",
    #"price": 9.00,
    #"currency": "EUR",

    "depends": [
        "website_sale",
        "payment"
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "website_sale_autopay_views.xml",
    ],
    "demo": [
    ],
    "installable": True,
    "auto_install": False,
}
