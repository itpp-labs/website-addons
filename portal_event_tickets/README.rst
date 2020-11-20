.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

=======================
 Customer Event Portal
=======================

Allows to customers see tickets for events at Portal.

* Only confirmed tickets with attendee_partner_id as current user are shown

Additional features:

* Ticket transferring feature

  * To decrease chance of transferring to a wrong email, partner with the email must exist before transferring.
  * New *When to Run* values for Email Schedule:

    * transferring_started
    * transferring_finished

  * New attendee receives email with a link to finish ticket transferring

* Tracks changes in key registration fields (via ``track_visibility='onchange'``)

* Tickets can be changed to other products (including other tickets)

  * When old ticket is canceled, a message with a reference to new Sale Order is posted

Relation to other modules
=========================

website_event_refund
--------------------

Ticket refunding feature based on ``website_event_refund`` module

website_event_attendee_signup
-----------------------------

It's recommended to use the module with ``website_event_attendee_signup`` which creates user for each attendee on registration.

website_event_attendee_fields
-----------------------------

We need this modules for autofill feature. Other features of the modules are optional.

website
-------

The module is not splitted in two where one doesn't depend on website how it's usually done (e.g. ``portal_event_tickets`` and ``website_portal_event_tickets``), because since 11.0 there is no such separation.

event_sale
----------

We don't split module in two where one doesn't depend on ``event_sale`` (e.g. ``portal_event_tickets`` and ``portal_event_tickets_sale``) for following reasons:

* it simplifies development and maintainance
* we don't consider portal module without ``event_sale`` as popular
* free events are still usable even if ``event_sale`` module is installed

portal_event
============

``portal_event`` should be more proper name for this module, but it's occupied by repository odoo/odoo and which makes it impossible to use it in odoo apps store.


Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Contributors
============
* `Ivan Yelizariev <https://it-projects.info/team/yelizariev>`__


Further information
===================

Odoo Apps Store: https://apps.odoo.com/apps/modules/10.0/portal_event_tickets/


Tested on `Odoo 10.0 <https://github.com/odoo/odoo/commit/6c1c1f6e9e03322771169b920d3c14c5e33111e9>`_
