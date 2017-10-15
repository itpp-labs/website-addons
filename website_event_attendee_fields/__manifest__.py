# -*- coding: utf-8 -*-
{
    "name": """Customizable fields for attendees on Events""",
    "summary": """Do you need more information about attendees than three default fields (name, email, phone)?""",
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
        "website_event",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/website_event_templates.xml",
        "views/event_event_views.xml",
        "security/ir.model.access.csv",
    ],
    "qweb": [
    ],
    "demo": [
        "data/event_event_attendee_field_demo.xml",
        "data/event_event_demo.yml",
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,
}
