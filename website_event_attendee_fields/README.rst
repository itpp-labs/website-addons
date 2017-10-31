=============================================
 Customizable fields for attendees on Events
=============================================

By default ``website_event`` module asks only three fields to fill about attendees (name, email, phone). This module allows to customize any set of fields.

Also,

* shows field name in input placeholder (it's neede when there are many fields per each attendee)
* depends on ``website_event_attendee_signup`` module to allow saving fields to ``res.partner`` model (signup feature is optional there)

  * TODO: probably we need to update module ``partner_event`` to avoid such dependency

* hides Header at Attendee form if total bootstrap width of field columns is more that 12

* If user is authenticated:

  * first attendee at the form will have autofilled values (if person is not registered yet)


Demo mode
---------
In demo installation:

* on installation each Event gets standarts fields (Name, Email, Phone) and two fields from partner (Country, Job Position)

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

Demo: http://runbot.it-projects.info/demo/website-addons/10.0

HTML Description: https://apps.odoo.com/apps/modules/10.0/website_event_attendee_fields/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 10.0 51861e889ab7c8795cccc3eaca27b90b62ceb89c
