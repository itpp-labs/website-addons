==========================
 Auto Sign Up Event guest
==========================

The modules creates ``res.user`` from every ``event.registration`` (*attendee*)
and calls ``signup_prepare()`` method to allow to send an email with signup url to access the portal.

The modules adds email template ``Event: Signup``, which can be used directly or as an example to modify other email template.

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

HTML Description: https://apps.odoo.com/apps/modules/12.0/website_event_attendee_signup/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 12.0 0aef3724c7772c99abdf8e9f850fc5289201ac6f
