=============================================
 Customizable fields for attendees on Events
=============================================

By default ``website_event`` module asks only three fields to fill about attendees (name, email, phone). This module allows to customize any set of fields.

Also,

* depends on ``website_event_attendee_signup`` module to allow saving fields to ``res.partner`` model (signup feature is optional there)

  * TODO: probably we need to update module ``partner_event`` to avoid such dependency

* if total bootstrap width of field columns is more that 12

  * hides Header at Attendee form
  * shows field name above each input

* If user is authenticated:

  * first attendee at the form will have autofilled values (if person is not registered yet)

* When email column is presented and there is a partner with that email:

  * if partner has registration for the event:

    * registration is blocked. Warning is shown

  * if partner has some of fields

    * grey them out with a message "This email address already has an account. Data will be taken from this account"

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
