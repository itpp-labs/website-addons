=======================
 Customer Event Portal
=======================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

See documentation for `website_event_attendee_fields <https://apps.odoo.com/apps/modules/12.0/website_event_attendee_fields/>`__

Ticket transferring configuration
---------------------------------

At event form:

* Activate ``[x] Enable Ticket transferring``
* At ``Email Schedule`` Tab add record:

  * **Email To Send**: *Event: Transferring started*
  * **Unit**: *Immediately*
  * **When to Run**: *Transferring started*

Ticket changing configuration
-----------------------------

At event form:

* Activate ``[x] Enable Ticket changing``

Usage
=====

* Open link ``/my``
* RESULT: there is sections Tickets

Ticket transferring
===================

Feature allows for attendees to transfer ticket ownership to another partner by email.

* Login to portal as current ticket attendee
* Select a ticket
* Click button ``[Transfer to another person]``
* Specify person's email. The partner must be already registered
* Click ``[Confrim]``

Now second person receives an email. If you use test deployment without mail servers, then you can find email at menu ``[[ Settings ]] >> Technical >> Email >> Messages``.

* Login to portal as new ticket attendee
* Open then link at email
* Fill the form
* Click ``[Confrim]``
* RESULT: Ticket has new owner

Ticket changing
===============

Feature allows to change the ticket to new ticket or product

* Login to portal
* Select a ticket
* Click button ``[Upgrade / Change ticket]``
* You are redirected to original event page. You can select new ticket or navigate to ``/shop`` page and fill the cart
* Follow checkout process
* When the order is confirmed (e.g. after payment), old ticket is canceled and new one is confirmed
