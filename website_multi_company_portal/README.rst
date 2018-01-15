=======================================
 Real Multi Website (portal extension)
=======================================

Multi Website support in Portal:

* update user's company_id value for portal user or internal users with when current company is in user's **Allowed companies** list. List of features that requires proper user's company_id value:

  * show orders, invoices, etc. only for current company
  * pay invoices via proper payment processor. See `search condition of acquirer_id in pay method <https://github.com/odoo/odoo/blob/10.0/addons/website_payment/controllers/main.py#L40-L42>`__.
  * don't get access error when download invoice via controller ``/report/pdf/account.report_invoice/123``

Credits
=======

Contributors
------------
* `Ivan Yelizariev <https://it-projects.info/team/yelizariev>`__

Sponsors
--------
* `IT-Projects LLC <https://it-projects.info>`__

Maintainers
-----------
* `IT-Projects LLC <https://it-projects.info>`__

      To get a guaranteed support you are kindly requested to purchase the module at `odoo apps store <https://apps.odoo.com/apps/modules/11.0/website_multi_company_portal/>`__.

      Thank you for understanding!

      `IT-Projects Team <https://www.it-projects.info/team>`__

Further information
===================

Demo: http://runbot.it-projects.info/demo/website-addons/11.0

HTML Description: https://apps.odoo.com/apps/modules/11.0/website_multi_company_portal/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 10.0 6b27d9f91a050ce5a8484fd53ba0bfcafe6d28c8
