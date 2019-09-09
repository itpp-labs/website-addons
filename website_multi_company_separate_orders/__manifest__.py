# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """Real Multi Website (eCommerce extension Customization)""",
    "summary": """Multi Website support in eCommerce Customization""",
    "category": "eCommerce",
    # "live_test_url": "http://apps.it-projects.info/shop/product/website-multi-company?version=12.0",
    "images": ["images/website_multi_company_sale_main.png"],
    "version": "12.0.1.5.1",
    "application": False,

    "author": "IT-Projects LLC, Kolushov Alexandr",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info/team/yelizariev",
    "license": "LGPL-3",
    "price": 9.00,
    "currency": "EUR",

    "depends": [
        "website_multi_company_sale",
        "website_sale",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/product_public_category_views.xml",
        "views/sale_views.xml",
        "views/website_views.xml",
        "views/templates.xml",
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
