========================
 Multi Website Delivery
========================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

* Open menu ``[[ Inventory ]] >> Configuration >> Delivery >> Delivery Methods``
* Open a delivery method form on ``Website`` tab
* Specify **Allowed websites** on which the delivery method will be available on. Specify none if you want it to be available on any website
* Make sure that you have checked the setting **Common Product Catalog** from ``[[ Settings ]] >> General Settings`` or configure all your delivery carriers so they have empty **Company** field

Usage
=====

* Make a purchase from website shop as usual
* RESULT: on the ``Payment`` stage of checkout process see that only allowed delivery methods are available for you
