======================
 Web Login Background
======================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way
* If you use Website app, you also need to install `website_login_background <https://apps.odoo.com/apps/modules/14.0/website_login_background/>`__

Configuration
=============

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* add several images:

  * From menu ``[[ Settings ]] >> Technical >> Database Structure >> Attachments`` create a new image attachment
  * In the attachment form put a checkmarks in the "Use as login page background" and the "Is public document" checkboxes and click on ``[Save]`` button

Usage
=====

* Open login page ``/web/login``
* RESULT: your image is on background
* Reload login page
* RESULT: background is randomly changed. It works only if there are more than one background images.
