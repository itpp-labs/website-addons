=====================================================
 Tickets purchasing: force user to sign in / sign up
=====================================================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Usage
=====

* Open page ``/event`` as non-authenticated user
* Select some Event
* RESULT:

  * button button ``[Register Now]`` (``[Order Now]`` if ``website_event_sale`` is installed) is renamed to ask for sign in / sign up
  * quantity selectors are disabled

* Click the button
* RESULT: it opens login page
* sign in or sign up
* RESULT: you are redirect back to event page and now you can order the tickets
