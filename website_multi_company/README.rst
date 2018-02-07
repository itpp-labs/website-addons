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

Multi-Theme
-----------

* New menu to allow switch theme to multi-theme on-flight (i.e. without adding code to the theme).
* Removes `restrictions <https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module.py#L387-L400>`__ for Theme category, i.e. allows to install several themes at once

Roadmap
=======

* Currently, all websites share the same footer. Posible solution: add field to ``res.company`` or ``website`` model and use that in template, e.g.::

    <div t-field="website.website_footer" class="oe_structure mt16"/>

* TODO: Create website.theme record automatically after theme installation (probably via inheriting ``button_install`` method)

Credits
=======

Contributors
------------
* Ivan Yelizariev <yelizariev@it-projects.info>

Sponsors
--------
* `IT-Projects LLC <https://it-projects.info>`__

Maintainers
-----------
* `IT-Projects LLC <https://it-projects.info>`__

Further information
===================

Demo: http://runbot.it-projects.info/demo/website-addons/10.0

HTML Description: https://apps.odoo.com/apps/modules/10.0/website_multi_company/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 10.0 ffba5c688ff74a0630f9f70be1d7760a43a7deba
