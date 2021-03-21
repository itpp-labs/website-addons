# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Multi Website e-Tickets""",
    "summary": """Configure Events' Tickets per website""",
    "category": "Marketing",
    # "live_test_url": "",
    "images": ["images/website_multi_company_event_sale.jpg"],
    "version": "11.0.1.0.0",
    "application": False,
    "author": "IT-Projects LLC, Ildar Nasyrov",
    "support": "apps@itpp.dev",
    "website": "https://twitter.com/OdooFree",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["website_multi_company", "website_event_sale", "ir_rule_website"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["views/event_views.xml", "security/event_security.xml"],
    "demo": [],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": False,
}
