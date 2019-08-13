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

Further information
===================

Demo: http://runbot.it-projects.info/demo/website-addons/12.0

HTML Description: https://apps.odoo.com/apps/modules/12.0/website_event_attendee_fields/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 12.0 fbc14ac649f80ff391f5a70ef41443111dff5739
