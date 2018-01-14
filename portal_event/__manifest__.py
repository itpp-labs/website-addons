# -*- coding: utf-8 -*-
{
    "name": """Portal Event""",
    "summary": """Allows to customers see their tickets for events at Portal""",
    "category": "Marketing",
    # "live_test_url": "",
    "images": [],
    "version": "1.0.0",
    "application": False,

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info/team/yelizariev",
    "license": "LGPL-3",
    # "price": 9.00,
    # "currency": "EUR",

    "depends": [
        "event_sale",
        "website_portal",
        "partner_event",
        "website_event_attendee_fields",
        "website_sale_refund",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/portal_templates.xml",
        "views/event_registration.xml",
        "views/event_event.xml",
        "data/mail_template_data.xml",
    ],
    "qweb": [
    ],
    "demo": [
        "views/assets_demo.xml",
        "data/res_users_demo.xml",
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": True,
}