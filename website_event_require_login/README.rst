=====================================================
 Tickets purchasing: force user to sign in / sign up
=====================================================

The module updates ``/event/EVENT-ID/register`` page when user is not authenticated:

* button ``[Register Now]`` (``[Order Now]`` if ``website_event_sale`` is installed) is renamed to ``[Sign in (Sign up) to proceed]`` and opens ``/web/login`` page
* quantity selectors are disabled

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

HTML Description: https://apps.odoo.com/apps/modules/10.0/website_event_sale_require_login/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 10.0 bbc226cd6cc17c69979f81831a3da8cc668bf064
