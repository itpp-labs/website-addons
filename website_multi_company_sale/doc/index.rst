==========================================
 Real Multi Website (eCommerce extension)
==========================================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

Follow instruction of the base module `Real Multi Website <https://www.odoo.com/apps/modules/11.0/website_multi_company/>`__.

Website Orders
--------------

* Open menu ``[[ Website ]] >> Configuration >> Websites``
* For each website configure **Salesperson** and **Sales Channel** fields
* RESULT: new orders made via website will be assigned to proper Salesperson and Sales Channel

Multi-categories
----------------

* Open menu ``[[ Website ]] >> Configuration >> Products >> eCommerce Categories``
* Only for top-level (i.e. without ``parent_id``) categories: specify **Websites** field

Multi-products
--------------
* Open menu ``[[ Sales ]] >> Sales >> Products``
* Specify **Allowed websites** for your products
* Websites company and product company should be equal. But if you want different company websites then leave the **Company** field empty in your product - in such case you can specify any websites

Multi-payment-acquirers
-----------------------
* Open menu ``[[ Website ]] >> Configuration >> eCommerce >> Payment Acquirers``
* Specify **Allowed websites** for your payment acquirer. If no website is specified then the acquirer will be available on any website with the same company
* Choosen websites companies and acquirer's company should be equal


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

Multi-products
--------------

* Open website shop
* RESULT: you should only see products allowed for this website or products with no websites specified

Multi-payment-acquirers
-----------------------

* Open website shop
* Buy a product
* On Payment step of checkout there should be available only specified acquirers
