.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

==========================
 Event guest Custom Field
==========================

By default ``website_event`` module asks only three fields to fill about attendees (name, email, phone). This module allows to customize any set of fields.

Also,

* if total bootstrap width of field columns is more that 12

  * hides Header at Attendee form
  * shows field name above each input

* If user is authenticated:

  * first attendee at the form will have autofilled values (if person is not registered yet)

* Handles cases of reusing email. See `<doc/index.rst>`__ for details

* Modifies behaviour of ``partner_event`` module:

  * always updates Registration's name and phone to corresponded values of Attendee Partner, because they may be taken from Partner record (e.g. Public User)

  * If attendee partner exists and current (authenticated) user is the attendee partner himself: update partner values. (We don't update fields always, because it leads to security issue: anyone can change partner name, passport, etc. just knowing his email). Default behaviour: only create partner if one doesn't exist.

* Prevents changing qty for event lines (TODO: move this to a separate module)
* Custom redirection after filling ticket form, e.g. to cart page to ask for coupons (TODO: move this to a separate module). Create System Parameter ``website_event_sale.redirection`` to configure it.

Demo mode
---------
In demo installation:

* on installation each Event gets standard fields (Name, Email, Phone) and two fields from partner (Country, Job Position)

Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Contributors
============
* `Ivan Yelizariev <https://it-projects.info/team/yelizariev>`__


Further information
===================

Odoo Apps Store: https://apps.odoo.com/apps/modules/10.0/website_event_attendee_fields/


Tested on `Odoo 10.0 <https://github.com/odoo/odoo/commit/51861e889ab7c8795cccc3eaca27b90b62ceb89c>`_
