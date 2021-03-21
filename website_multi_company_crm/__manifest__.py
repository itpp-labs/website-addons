# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Real Multi Website (CRM extension)""",
    "summary": """Make CRM features work properly in multi-website environment""",
    "category": "eCommerce",
    # "live_test_url": "http://apps.it-projects.info/shop/product/website-multi-company?version=11.0",
    "images": ["images/main.jpg"],
    "version": "13.0.1.0.0",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@itpp.dev",
    "website": "https://twitter.com/OdooFree",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["crm", "website_multi_company"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["views/crm_lead_views.xml", "security/crm_lead_security.xml"],
    "qweb": [],
    "demo": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": False,
}
