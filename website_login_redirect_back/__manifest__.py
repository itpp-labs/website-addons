# Copyright 2020 Ildar Nasyrov <iledarn@gmail.com.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Website Login Redirect Back",
    "summary": "Redirects the user at the same page from where she logs in",
    "version": "13.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/iledarn",
    "author": "iledarn",
    "license": "Other OSI approved licence",  # MIT
    "application": False,
    "installable": True,
    "depends": ["website"],
    "data": [
        "views/webclient_templates.xml",
        "views/portal_templates.xml",
    ],
}
