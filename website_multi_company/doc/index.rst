====================
 Real Multi Website
====================

Installation
============

`Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way.

dbfilter
--------

No updates in odoo config is required if you use only one database. But for multi-database
instance odoo has to know which database to use when handle new request without
session information. There are two ways to do it:

* Let user select database manually (bad user experience)
* Take database depending on host name (prefered)

In the latter case ``dbfilter`` is used, though it's not flexible enough.

For TESTING purpose you can use the following configuration:

* dbfilter: ^%d$
* database name: example

  * host names:
  
    * example.shop1.local
    * example.shop2.local
    * example.shop3.local

For PRODUCTION we recommend to use single database installation or make modification in odoo/http.py file as following::

    # updated version of db_filter
    def db_filter(dbs, httprequest=None):
        httprequest = httprequest or request.httprequest
        h = httprequest.environ.get('HTTP_HOST', '').split(':')[0]
        d, _, r = h.partition('.')
        t = r
        if d == "www" and r:
            d, _, t = r.partition('.')
        r = odoo.tools.config['dbfilter'].replace('%h', h).replace('%d', d).replace('%t', t)
        dbs = [i for i in dbs if re.match(r, i)]

Then you can use following configuration

* dbfilter: ^%t$
* database name: example.com

  * host names:
  
    * shop1.example.com
    * shop2.example.com
    * shop3.example.com

* database name: example.org

  * host names:
  
    * shop1.example.org
    * shop2.example.org
    * shop3.example.org

Configuration
=============

* `Enable technical features <https://odoo-development.readthedocs.io/en/latest/odoo/usage/technical-features.html>`__
* At ``Settings >> Users`` menu and activate **Multi Companies** and set **Allowed Companies**
* Open menu ``Website Admin >> Configuration >> Websites``
* Create or select a website record
* Update fields:

  * **Website Domain** -- website address, e.g. *shop1.example.com*
  * **Company** -- which company is used for this *website*

Website Menus
-------------

You can edit, duplicate or create new menu at ``Website Admin >> Configuration >> Website Menus`` -- pay attention to fields **Website**, **Parent Menu**. In most cases, **Parent Menu** is a *Top Menu* (i.e. menu record without **Parent Menu** value). If a *website* doesn't have *Top Menu* you need to create one.

Note. Odoo doesn't share Website Menus (E.g. Homepage, Shop, Contact us, etc.) between websites. So, you need to have copies of them.

Usage
=====

For all examples below:

* configure some WEBSITE1 for HOST1 and COMPANY1
* configure some WEBSITE2 for HOST2 and COMPANY2


Steps for Website
-----------------

* open HOST1/
* add Text block "text1" to Home Page
* open HOST2/ -- you don't see "text1"
* add Text block "text2" to Home Page
* open HOST1/ -- you see "text1" and don't see "text2"

The same works if you create new page, new menu

Steps for eCommerce
-------------------

* install ``website_shop`` (eCommerce) module
* open ``Invoicing >> Configuration >> Payments Acquirers`` and create payments acquirers per each company

  * use ``[Action] -> Duplicate`` button
  * don't forget to click ``[Unpublished On Website]`` button to activate it

* open ``Sales >> Products`` and create product per each company if they don't exist
* open HOST1/shop, make order, open backend -- created order belongs to COMPANY1
* open HOST2/shop, make order, open backend -- created order belongs to COMPANY2
