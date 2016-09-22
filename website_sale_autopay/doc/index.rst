======================
 Website sale autopay
======================

Installation
============

* For multi-company support install additional module: https://github.com/OCA/website/tree/8.0/website_sale_order_company

Configuration
=============

* Install ``payment_`` module that you need to use in website shop, e.g. payment_paypal.
* From ``Settings / Payments / Payment Acquirers`` create payment acquirers.

  * In acquirer configuration select proper payment method

* For multi-company:

  * Define company for each of your products.
  * Create accounts from ``Settings / Configuration / Invoicing`` menu:

    * select template
    * select currency. WARNING: select the same currency for all companies
    * push ``[Apply]`` button

  * Create payment acquirers for each company you have.

    * In acquirer configuration select proper payment method
 
Usage
=====

* Put some products in your shopping cart from website shop
* Pay for them. You can use test paypal payments for that purpose https://odoo-development.readthedocs.io/en/latest/dev/tests/paypal.html
* From ``Sale / Sale Order`` find sale order representing your test shopping
* You can see that the sale order have invoice and it is already in ``paid`` state
