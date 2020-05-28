.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

====================
 Website Sale Cache
====================

The module allows to cache product website categories and significantly accelerate the page loading with a large number
of product categories.

When multiple odoo workers are used, the cache is updated for each one separately. So the page may be loaded slowly
before updating the cache for each worker. Once the latter is done, the page will be loading faster,
as far as the advantages of caching allow.

The speed is not increased at the first load, because the data has not been cached yet.
You need to expand each category in shop to cache the page in both collapsed and non collapsed.
After update the list of
categories (deleting a category, updating or creating a new one), the cache is updated and once again the speed
will increase only after the first load.

Warning
-------
Cache is updated every time on creation, editing or deletion the product public category model instance.
This can lead to issues, e. g. when importing a large number of categories.
It is recommended to temporarily uninstall the module in this case.

Roadmap
-------

* TODO: deal with too many cache options that can cause memory loss

Credits
=======

Contributors
------------
* Artyom Losev <apps@it-projects.info>
* Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>

Sponsors
--------
* `IT-Projects LLC <https://it-projects.info>`__

Maintainers
-----------
* `IT-Projects LLC <https://it-projects.info>`__

      To get a guaranteed support you are kindly requested to purchase the module at `odoo apps store <https://apps.odoo.com/apps/modules/12.0/website_sale_cache/>`__.

      Thank you for understanding!

      `IT-Projects Team <https://www.it-projects.info/team>`__

Further information
===================

Demo: http://runbot.it-projects.info/demo/website-addons/12.0

HTML Description: https://apps.odoo.com/apps/modules/12.0/website_sale_cache/

Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_

Tested on Odoo 12.0 97f89dc0484902c58dec5dbb9de65f17661163f4
