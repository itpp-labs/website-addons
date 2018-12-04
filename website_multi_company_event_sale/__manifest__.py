# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": """Real Multi Website (Online Event's Tickets extension)""",
    "summary": """Configure Events' Tickets per website""",
    "category": "Marketing",
    # "live_test_url": "",
    "images": ['images/website_multi_company_event_sale.jpg'],
    "version": "10.0.1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Ildar Nasyrov",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info/team/iledarn",
    "license": "LGPL-3",
    "price": 19.00,
    "currency": "EUR",

    "depends": [
        "website_multi_company",
        "website_event_sale",
        "ir_rule_website",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/event_views.xml",
        "security/event_security.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": False,
}
