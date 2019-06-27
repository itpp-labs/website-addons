====================
 Real Multi Website
====================

Allows to set up multi-website and handles requests in a different company context. Later is especially useful for eCommerce to make orders for a different companies.

Odoo is designed to switch website by host name, but this feature is not completed and not supported. This module fills the gap.

Implementation
==============

Websites
--------

To work with ``website`` model, the module adds menu ``Website Admin >> Configuration >> Websites``.

To have unique home page per each website, the module makes duplicates of ``website.homepage``, e.g. ``website.homepage2`` for company #2.

To fix company logo (left side of top menu), the url is updated from ``/logo.png`` to ``/logo.png?company=ID``.

Website Menus
-------------

To easy work with ``website.menu`` model, the module adds menu ``Website Admin >> Configuration >> Website Menus`` and adds form view.

eCommerce
---------

Updates for eCommerce:

* ``/shop/*`` pages show only products for current company

Roadmap
=======

* TODO: Create website.theme record automatically after theme installation (probably via inheriting ``button_install`` method)

Credits
=======

Contributors
------------
* Ivan Yelizariev <yelizariev@it-projects.info>

Sponsors
--------
* `e-thos SSII <http://www.e-thos.fr/>`__

Maintainers
-----------
* `IT-Projects LLC <https://it-projects.info>`__

      To get a guaranteed support you are kindly requested to purchase the module at `odoo apps store <https://apps.odoo.com/apps/modules/12.0/website_multi_company/>`__.

      Thank you for understanding!

      `IT-Projects Team <https://www.it-projects.info/team>`__

Further information
===================

Demo: http://runbot.it-projects.info/demo/website-addons/12.0

HTML Description: https://apps.odoo.com/apps/modules/12.0/website_multi_company/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 12.0 0669eddc7e88303f3a97e9f4f834f64fd9a8158c
