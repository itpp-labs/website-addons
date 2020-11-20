.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

=================
 Multi Ecommerce
=================

Multi Website support in eCommerce:

* adds field ``website_ids`` to payment.acquirer
* adds field ``website_ids`` to product.template
* adds field ``website_ids`` to product.public.category
* use separate sale order (cart) for different companies -- works by adding ``company_dependent`` attribute to ``last_website_so_id`` field
* different pricelist (and currency) for different website:

  * to avoid problems with Public User on websites that belong to different
    companies, the module disables multi-company access rules for pricelist.
    Alternative to this might be a new module that disables some rules for
    Public User only
  * workaround for authenticated user is filtering pricelists by website in ``_get_partner_pricelist`` method

Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Contributors
============
* `Ivan Yelizariev <https://it-projects.info/team/yelizariev>`__

===================

Odoo Apps Store: https://apps.odoo.com/apps/modules/11.0/website_multi_company_sale/


Tested on `Odoo 11.0 <https://github.com/odoo/odoo/commit/f34d4d33a09d33a12e427c2490b6526546114486>`_
