# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """Real Multi Website""",
    "summary": """Yes, you can set up multi-company, multi-website, multi-theme, multi-eCommerce on a single database!""",
    "category": "eCommerce",
    # "live_test_url": "http://apps.it-projects.info/shop/product/website-multi-company?version=12.0",
    "images": ['images/website_multi_company_main.png'],
    "version": "12.0.3.0.1",
    "application": False,

    "author": "IT-Projects LLC, Ivan Yelizariev, Nicolas JEUDY",
    "support": "apps@it-projects.info",
    "website": "https://twitter.com/yelizariev",
    "license": "LGPL-3",
    "price": 200.00,
    "currency": "EUR",

    "depends": [
        "mail_multi_website",
        "website",
        "ir_config_parameter_multi_company",
        "ir_rule_website",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/website_views.xml",
        "views/website_menu_views.xml",
        "views/res_config_views.xml",
        "views/website_navbar_templates.xml",
        "views/res_users_view.xml",
        "data/first_action.xml",
        'security/res_security.xml',
    ],
    "qweb": [
    ],
    "demo": [
        "data/demo.xml",
    ],

    "post_load": "post_load",
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,

    "demo_title": "Real Multi Website",
    "demo_addons": [
        "website_multi_company_sale",
        "website_multi_company_portal",
    ],
    "demo_addons_hidden": [
        "website_multi_company_demo",
    ],
    "demo_url": "website-multi-company",
    "demo_summary": "The module allows to set up multi-company, multi-website, multi-theme, multi-eCommerce on a single database!",
    "demo_images": [
        "images/website_multi_company_main.png",
    ]
}
