==========================================
 Real Multi Website (eCommerce extension)
==========================================

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

      To get a guaranteed support you are kindly requested to purchase the module at `odoo apps store <https://apps.odoo.com/apps/modules/11.0/website_multi_company_sale/>`__.

      Thank you for understanding!

      `IT-Projects Team <https://www.it-projects.info/team>`__

Further information
===================

Demo: http://runbot.it-projects.info/demo/website-addons/11.0

HTML Description: https://apps.odoo.com/apps/modules/11.0/website_multi_company_sale/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 11.0 f34d4d33a09d33a12e427c2490b6526546114486
