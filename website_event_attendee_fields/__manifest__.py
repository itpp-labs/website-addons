# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2019 Ruslan Ronzhin <https://it-projects.info/team/rusllan/>
# Copyright 2019 Artem Rafailov <https://it-projects.info/team/Ommo73/>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Event guest Custom Field""",
    "summary": """Do you need more information about attendees than three default fields (name, email, phone)?""",
    "category": "Marketing",
    # "live_test_url": "http://apps.it-projects.info/shop/product/portal-event-tickets?version=10.0",
    "images": ["images/banner.jpg"],
    "version": "12.0.2.0.2",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@itpp.dev",
    "website": "https://it-projects.info/team/yelizariev",
    "license": "Other OSI approved licence",  # MIT
    "price": 200.00,
    "currency": "EUR",
    "depends": ["website_event_sale", "website_event", "partner_event"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "data/event_event_attendee_field_demo.xml",
        "views/website_event_templates.xml",
        "views/event_event_views.xml",
        "security/ir.model.access.csv",
        "views/assets.xml",
    ],
    "qweb": [],
    "demo": ["views/assets_demo.xml"],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "auto_install": False,
    "installable": False,
}
