# -*- coding: utf-8 -*-
{
    "name": """Real Multi Website""",
    "summary": """Yes, you can set up multi-company, multi-website, multi-theme, multi-eCommerce on a single database!""",
    "category": "eCommerce",
    "live_test_url": "http://apps.it-projects.info/shop/product/website-multi-company?version=10.0",
    "images": ['images/website_multi_company_main.png'],
    "version": "1.1.0",
    "application": False,

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@it-projects.info",
    "website": "https://twitter.com/yelizariev",
    "license": "LGPL-3",
    "price": 400.00,
    "currency": "EUR",

    "depends": [
        "website",
        "website_multi_theme",
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

    "demo_title": "Real Multi Website",
    "demo_addons": [
    ],
    "demo_addons_hidden": [
        "website_multi_company_demo",
    ],
    "demo_url": "website-multi-company",
    "demo_summary": "The module allows to set up multi-company, multi-website, multi-theme, multi-eCommerce on a single database!",
    "demo_images": [
        "images/website_multi_company_main.png",
        "static/description/icon.png",
        "static/description/website_apple.png",
        "static/description/website_commerce1.png",
        "static/description/website_commerce2.png",
        "static/description/website_commerce3.png",
        "static/description/website_form.png",
        "static/description/website_menus.png",
        "static/description/website_samsung.png",
        "static/description/website_so1.png",
        "static/description/website_so1_1.png",
        "static/description/website_so2.png",
        "static/description/website_so2_1.png",
        "static/description/website_so3.png",
        "static/description/website_so3_1.png",
        "static/description/website_xiaomi.png",
        "static/description/website_menu.png",
    ]
}
