{
    "name": """Hide "Add To Cart" button from product page""",
    "summary": """Allows to disable product sales via eCommerce for any reason""",
    "category": "eCommerce",
    "images": [],
    "version": "1.0.0",

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info",
    "license": "LGPL-3",
    # "price": 9.00,
    # "currency": "EUR",

    "depends": [
        "website_sale",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views.xml",
        "templates.xml",
    ],
    "qweb": [
    ],
    "demo": [
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": False,
    "auto_install": False,
}
