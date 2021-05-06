# Copyright 2020 Ildar Nasyrov <iledarn@gmail.com.com>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": "Login Page Redirection",
    "summary": "Redirects portal user to the page which was right before authentication",
    "version": "13.0.1.0.0",
    "category": "Website",
    "website": "https://twitter.com/OdooFree",
    "author": "IT Projects Labs, Ildar Nasyrov",
    "license": "Other OSI approved licence",  # MIT
    "application": False,
    "installable": True,
    "depends": ["website"],
    "data": [
        "views/webclient_templates.xml",
        "views/portal_templates.xml",
    ],
}
