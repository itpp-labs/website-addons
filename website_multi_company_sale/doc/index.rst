==========================================
 Real Multi Website (eCommerce extension)
==========================================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

Follow instruction of the base module `Real Multi Website <https://www.odoo.com/apps/modules/11.0/website_multi_company/>`__.

Multi-categories
----------------
* Open menu ``[[ Website Admin ]] >> Configuration >> Products >> eCommerce Categories``
* Specify **Websites** fields to parent categories.

Usage
=====

Multi-categories
----------------

* Open shop at some of your websites
* Login as Administrator
* In ``Customize`` section activate ``[x] eCommerce Categories``
* RESULT: parent categories for current website and categories without value at **Websites** fields are shown only. **Websites** value of child categories are ignored.

Multi-cart
----------

* Login as portal or internal user at some of your websites
* Add some products to the cart
* Open another website that belongs to another company
* Login as the same user
* RESULT: you have empty cart, rather than one from previous website
