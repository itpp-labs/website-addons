.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

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

The speed is not increased at the first load, because the data has not been cached yet. After update the list of
categories (deleting a category, updating or creating a new one), the cache is updated and once again the speed
will increase only after the first load.

Warning
-------
Cache is updated every time on creation, editing or deletion the product public category model instance.
This can lead to issues, e. g. when importing a large number of categories.
It is recommended to temporarily uninstall the module in this case.

Questions?
==========

To get an assistance on this module contact us by email :arrow_right: help@itpp.dev

Contributors
============
* Artyom Losev <apps@it-projects.info>
* Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>

===================

Odoo Apps Store: https://apps.odoo.com/apps/modules/10.0/website_sale_cache/


Tested on `Odoo 10.0 <https://github.com/odoo/odoo/commit/1ffe85f1cb3defcbf932138e2fc13f3a81b34787>`_
