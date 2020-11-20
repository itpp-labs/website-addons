.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

======================
 Multi Website Portal
======================

Multi Website support in Portal:

* update user's company_id value for portal user or internal users with when current company is in user's **Allowed companies** list. List of features that requires proper user's company_id value:

  * show orders, invoices, etc. only for current company
  * pay invoices via proper payment processor. See `search condition of acquirer_id in pay method <https://github.com/odoo/odoo/blob/10.0/addons/website_payment/controllers/main.py#L40-L42>`__.
  * don't get access error when download invoice via controller ``/report/pdf/account.report_invoice/123``

Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Contributors
============
* `Ivan Yelizariev <https://it-projects.info/team/yelizariev>`__

===================

Odoo Apps Store: https://apps.odoo.com/apps/modules/11.0/website_multi_company_portal/


Tested on `Odoo 11.0 <https://github.com/odoo/odoo/commit/cae336478391f53b1d66644337da4152c8cbc14a>`_
