==================
Website sale cache
==================

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

Credits
=======

Contributors
------------
* Artyom Losev <losev@it-projects.info>

Sponsors
--------
* `IT-Projects LLC <https://it-projects.info>`__

Maintainers
-----------
* `IT-Projects LLC <https://it-projects.info>`__

Further information
===================
Usage instructions: `<doc/index.rst>`_

Changelog: `<doc/changelog.rst>`_
