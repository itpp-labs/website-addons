==================================
 Auto invoice creation on payment
==================================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

* Set acquirers:
    * Using administrator user go to ``Settings / Payments / Payments Acquirers``.
    * Set ``Journal`` for every acquirer to be used for eCommerce payments registration.


Usage
=====

When payment is processed thru some provider (acquirer), such as PayPal,
the invoice (Account voucher) is created with corresponding accounting entries.
You can look up created vouchers in ``Accounting / Journal Entries / Journal Vouchers``
(using user with `Technical Features <https://odoo-development.readthedocs.io/en/latest/odoo/usage/technical-features.html>`__ enabled and with Accountant rights) to see those payments.
