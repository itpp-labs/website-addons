{
    "name": """Customer Event Portal""",
    "summary": """Allows to customers see their tickets for events at the Portal""",
    "category": "Marketing",
    # "live_test_url": "http://apps.it-projects.info/shop/product/portal-event-tickets?version=10.0",
    "images": ["images/banner.jpg"],
    "version": "10.0.1.1.1",
    "application": False,

    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@it-projects.info",
    "website": "https://it-projects.info/team/yelizariev",
    "license": "LGPL-3",
    "price": 150.00,
    "currency": "EUR",

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
    "installable": False,

    "demo_title": "Event extensions",
    "demo_addons": ["website_event_attendee_fields", "website_event_attendee_signup", "website_event_require_login"],
    "demo_addons_hidden": ["website_event_attendee_fields_custom"],
    "demo_url": "portal-event-tickets",
    "demo_summary": "Set of modules to extend Event application.",
    "demo_images": [
    ]
}
