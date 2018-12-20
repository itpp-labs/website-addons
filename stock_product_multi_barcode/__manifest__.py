# Copyright 2018 {DEVELOPER_NAME} <https://it-projects.info/team/{DEVELOPER_GITHUB_USERNAME}>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": """Vendor Product Multiple Barcode""",
    "summary": """Vendor Product Multiple Barcode""",
    "category": "Warehouse",
    # "live_test_url": "http://apps.it-projects.info/shop/product/DEMO-URL?version={ODOO_BRANCH}",
    "images": [],
    "version": "11.0.1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Kolushov Alexandr",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info/team/KolushovAlexandr",
    "license": "LGPL-3",
    # "price": 9.00,
    # "currency": "EUR",

    "depends": [
        "stock_picking_barcode",
        "purchase",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/models_views.xml",
        "views/barcode_views.xml",
        "views/assets.xml",
    ],
    "demo": [
    ],
    "qweb": [
        'static/src/xml/picking.xml',
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": True,

    # "demo_title": "{MODULE_NAME}",
    # "demo_addons": [
    # ],
    # "demo_addons_hidden": [
    # ],
    # "demo_url": "DEMO-URL",
    # "demo_summary": "{SHORT_DESCRIPTION_OF_THE_MODULE}",
    # "demo_images": [
    #    "images/MAIN_IMAGE",
    # ]
}
