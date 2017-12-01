==============
 Portal Event
==============

Allows to customers see tickets for events at Portal.

website_event_attendee_signup
-----------------------------

It's recommended to use this module with ``website_event_attendee_signup`` which creates user for each attendee on registration.

website_portal_event
--------------------

The module is not splitted in two where one doesn't depend on website how it's usually done (e.g. ``portal_event`` and ``website_portal_event``), because since 11.0 there is no such separation.

event_sale
----------

We don't split module in two where one doesn't depend on ``event_sale`` (e.g. ``portal_event`` and ``portal_event_sale``) for following reasons:

* it simplifies development and maintainance
* we don't consider portal module without ``event_sale`` as popular
* free events are still usable even if ``event_sale`` module is installed


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

HTML Description: https://apps.odoo.com/apps/modules/10.0/portal_event/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 10.0 6c1c1f6e9e03322771169b920d3c14c5e33111e9
