===================================
 Sign-up event attendees to portal
===================================

The modules creates ``res.user`` from every ``event.registration`` (*attendee*) and sends link to finish registration at portal.

Also, the module does following:

* Introduces new field ``agent_id`` (``res.partner``) to ``event.registration`` and sets it to the partner who created (purchased) the registration
* Modifies behaviour of ``event_partner`` module:

  * create partner if Contact's email (``partner_id.email`` in ``event.registration``) differs from attendees email (``email`` in ``event.registration``)


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

HTML Description: https://apps.odoo.com/apps/modules/10.0/website_event_attendee_signup/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 10.0 c5df78f38bd476bc225778d1c30ff3061e9b23bc
