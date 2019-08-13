# Copyright 2017-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2019 Ruslan Ronzhin <https://it-projects.info/team/rusllan/>
# Copyright 2019 Artem Rafailov <https://it-projects.info/team/Ommo73/>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Auto Sign Up Event guest""",
    "summary": """Attendees can use portal dashboard to make extra purchases for the event, for example.""",
    "category": "Marketing",
    # "live_test_url": "http://apps.it-projects.info/shop/product/portal-event-tickets?version=10.0",
    "images": ["images/banner.jpg"],
    "version": "12.0.1.0.0",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@itpp.dev",
    "website": "https://it-projects.info/team/yelizariev",
    "license": "Other OSI approved licence",  # MIT
    "price": 190.00,
    "currency": "EUR",
    "depends": ["event", "partner_event"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["views/event_event_views.xml", "data/mail_template_data.xml"],
    "qweb": [],
    "demo": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "auto_install": False,
    "installable": True,
}
