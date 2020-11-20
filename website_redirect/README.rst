.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by IT Projects Labs
   :target: https://itpp.dev

Page redirections
=================

The module allows configure redirections rules. E.g.

    /contactus.php -> /page/website.contactus

unix-style wildcards can be used: https://docs.python.org/2/library/fnmatch.html

Tested on `Odoo 8.0 <https://github.com/odoo/odoo/commit/ea60fed97af1c139e4647890bf8f68224ea1665b>`_

Odoo 11.0+
----------

The feature is built-in since 11.0:

* Activate developer mode
* open ``[[ Website ]] >> Configuration >> Redirect``
