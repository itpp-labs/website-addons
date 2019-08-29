# Copyright 2018 Dinar Gabbasov <https://it-projects.info/team/GabbasovDinar>
# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """Upload Multiple Images at Once""",
    "summary": """Great tool to upload multiple images at once""",
    "category": "Extra Tools",
    # "live_test_url": "http://apps.it-projects.info/shop/product/multi-product-images?version=11.0",
    "images": ["images/multi_images_main.jpg"],
    "version": "11.0.1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Dinar Gabbasov, Kolushov Alexandr",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info/team/GabbasovDinar",
    "license": "LGPL-3",
    "price": 30.00,
    "currency": "EUR",

    "depends": [
        "website_sale",
        "web_multi_attachment_base",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/view.xml",
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
    "installable": False,

    "demo_title": "Upload Multiple Images at Once",
    "demo_addons": [
    ],
    "demo_addons_hidden": [
    ],
    "demo_url": "multi-product-images",
    "demo_summary": "Upload Multiple Images at Once",
    "demo_images": [
        "images/multi_images_main.jpg",
    ]
}
