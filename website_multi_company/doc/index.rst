====================
 Real Multi Website
====================

.. contents::
   :local:

Installation
============

Dependencies
------------
::

    apt-get install ruby-compass
    gem install compass bootstrap-sass

Odoo version
------------
Please use up-to-date version of odoo or at least be sure, that your odoo has following updates:

* 26 Jun 2018: https://github.com/odoo/odoo/commit/5cecd0a197eba847e4a71bea3a31584d2b88ea6b

Additional modules
------------------

Due to technical reasons some multi-website features are located in separate modules, install them depending on your needs:

* if you use ``website_sale`` (eCommerce) module, then install `Real Multi Website (eCommerce extension) <https://www.odoo.com/apps/modules/11.0/website_multi_company_sale/>`__ too
* if you use ``website_portal`` (Portal) module, then install `Real Multi Website (portal extension) <https://www.odoo.com/apps/modules/11.0/website_multi_company_portal/>`__ too

Domain Names
------------

You will be able to use any website domain names (not only subdomains), e.g. shop1.com, shop2.com, etc. In this case you need to setup DNS entries on your DNS hosting provider.

For example:

* shop1.com::

	@   A   your_server_ip_address

* shop2.com::

	@   A   your_server_ip_address

Web Server
----------
Your webserver (e.g. Apache or Nginx) must pass header ``Host`` to odoo, otherwise there is no way to define which website is used. Required configuration for Nginx and Apache looks as following:

Nginx::

        proxy_set_header Host $host;

Apache::

        ProxyPreserveHost On


Single database deployment
--------------------------

No updates in odoo config is required if you use only one database.

Multi database deployment
-------------------------
For multi-database instance odoo has to know which database to use when handle new request without
session information. There are two ways to do it:

* Let user select database manually (bad user experience)
* Take database depending on host name (prefered)

In the latter case ``dbfilter`` is usually used, though it's not flexible enough.

Using dbfilter parameter
~~~~~~~~~~~~~~~~~~~~~~~~
For TESTING purpose you can use the following configuration:

* dbfilter: ^%d$
* database name: example

  * host names:

    * example.shop1.local
    * example.shop2.local
    * example.shop3.local

Patching http.py
~~~~~~~~~~~~~~~~

For PRODUCTION deployment with websites on subdomains you can use following patch. You need to update odoo/http.py file as following::

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

Using dbfilter_from_header module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Most flexible way to deploy multi-database system is using `dbfilter_from_header <https://www.odoo.com/apps/modules/10.0/dbfilter_from_header/>`__ (check module description for installation instruction).

In short, you need to add special line to your webserver config (other webservers are supported too - see description of ``dbfilter_from_header``):

Nginx::

    proxy_set_header X-Odoo-dbfilter [your filter regex]

Apache::

    Header add X-ODOO_DBFILTER [your filter regex]
    RequestHeader add X-ODOO_DBFILTER [your filter regex]

Note, that you probably need to set usual ``db_filter`` to ``.*``, because ``dbfilter_from_header`` module uses that filter first and then applies filter from header.

Example (we use top level domain ``.example`` due to copyright issues, but it could be any top level domains at any combinations):

* dbfilter: .*
* database name: software_business

  * host names:

    * miscrosoft-products.example
    * antivirus.example
    * android.antivirus.example

* database name: delivery_business

  * host names:

    * pizzas.example
    * china-food.example

* Nginx::

      server {
        listen 80;
        server_name miscrosoft-products.example antivirus.example android.antivirus.example;

        proxy_set_header Host $host;
        proxy_set_header X-Odoo-dbfilter ^software_business\Z;

        location /longpolling {
            proxy_pass http://127.0.0.1:8072;
        }

        location / {
            proxy_pass http://127.0.0.1:8069;
        }
      }

      server {
        listen 80;
        server_name pizzas.example china-food.example;

        proxy_set_header Host $host;
        proxy_set_header X-Odoo-dbfilter ^delivery_business\Z;

        location /longpolling {
            proxy_pass http://127.0.0.1:8072;
        }

        location / {
            proxy_pass http://127.0.0.1:8069;
        }
       }

Apache::

       <VirtualHost *:80>
	       ServerName miscrosoft-products.example antivirus.example android.antivirus.example

		   ProxyPreserveHost On
		   Header add X-ODOO_DBFILTER "software_business"
           RequestHeader add X-ODOO_DBFILTER "software_business"

		   ProxyPass /   http://127.0.0.1:8069/
		   ProxyPassReverse /   http://127.0.0.1:8069/

		   ProxyPass /longpolling/   http://127.0.0.1:8072/longpolling/
		   ProxyPassReverse /longpolling/   http://127.0.0.1:8072/longpolling/

       </VirtualHost>

       <VirtualHost *:80>
           ServerName pizzas.example china-food.example

		   ProxyPreserveHost On
		   Header add X-ODOO_DBFILTER "delivery_business"
           RequestHeader add X-ODOO_DBFILTER "delivery_business"

           ProxyPass /   http://127.0.0.1:8069/
		   ProxyPassReverse /   http://127.0.0.1:8069/

		   ProxyPass /longpolling/   http://127.0.0.1:8072/longpolling/
		   ProxyPassReverse /longpolling/   http://127.0.0.1:8072/longpolling/

       </VirtualHost>

Odoo.sh deployment
------------------

In the manager of your domain name registrar you need to add CNAME records for your domains (subdomains), for example:

* Create a CNAME record ``shop1.example.org`` pointing to <yourdatabase>.odoo.com
* Create a CNAME record ``shop2.example.org`` pointing to <yourdatabase>.odoo.com
* Create a CNAME record ``example.com`` pointing to <yourdatabase>.odoo.com

Similar for dev and staging database, but use corresponding domain in odoo.com, e.g. ``mywebsite-master-staging-12345689.dev.odoo.com``

Translation issue
-----------------

Check this section if you use translations in odoo.

Odoo `may have wrong translations <https://github.com/odoo/odoo/issues/25550#issuecomment-401897456>`__, which leads to the error ``Translation is not valid``. You need either fix the translations or apply following workaround:

* open file ``odoo/addons/base/ir/ir_translation.py``
* comment out ``@api.constraints...`` near ``def _check_value``, that is you shall get something like this (pay attention to ``#`` symbol)::

    #@api.constrains('type', 'name', 'value')
    def _check_value(self):
        for trans in self.with_context(lang=None):

Configuration
=============

* `Enable technical features <https://odoo-development.readthedocs.io/en/latest/odoo/usage/technical-features.html>`__
* At ``[[ Settings ]] >> Users >> Users`` menu and activate **Multi Companies** and set **Allowed Companies**
* Open menu ``[[ Website ]] >> Configuration >> Websites``
* Create or select a website record
* Update fields:

  * **Website Domain** -- website address, e.g. *shop1.example.com*
  * **Company** -- which company is used for this *website*
  * **Favicon** -- upload website favicon
  * **Base Url** -- Currently it's used only for switching between websites on frontend. You must specify entire URL with http:// or https:// depending on whether your connection secured or not, for example:

    * http://shop1.example.com/
    * http://shop1.example.com/
    * https://shop2.example.com/

  * **Multi Theme** -- select a theme you wish to apply for website, e.g. *theme_bootswatch*

    * Click on **Reload Themes** button before using new theme
    * For unofficial themes extra actions are required as described `below <#multi-theme>`__

Website Menus
-------------

You can edit, duplicate or create new menu at ``[[ Website ]] >> Configuration >> Menus`` -- pay attention to fields **Website**, **Parent Menu**. In most cases, **Parent Menu** is a *Top Menu* (i.e. menu record without **Parent Menu** value). If a *website* doesn't have *Top Menu* you need to create one.

Note. Odoo doesn't share Website Menus (E.g. Homepage, Shop, Contact us, etc.) between websites. So, you need to have copies of them.

Multi-theme
-----------

After installing theme, navigate to ``[[ Website ]] >> Configuration >> Multi-Themes``. Check that the theme is presented in the list, otherwise add one.

Note: themes that depend on ``theme_common`` don't work in demo installation. To avoid this, you have to create database without demo data or comment out demo files in ``__manifest__.py`` file of ``theme_common`` module like this::

  'demo': [
       # 'demo/demo.xml',
    ],

Convert view to multi-website view
----------------------------------

When you have custom module which adds some page, you can easily convert to a multi-website view, i.e. it will have different versions of the page per each website. There are two ways to do that.

Convert to multi-website view via Editor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Open some page in Frontend with Developer Mode activated, e.g. ``/?debug``
* Click ``Customize -> HTML/CSS Editor``
* Select some view without suffix *(Website #...)*
* Click button ``[Convert to Multi-Website]``

Convert to multi-website view via Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You need to know so called *xml_id*, which has following format: `<MODULE_NAME>.<VIEW_NAME>`. Once you know that do as following:

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Navigate to ``[[ Website ]] >> Configuration >> Multi-Themes``
* Choose *Default Theme*
* In **Views** fields use *Create and Edit...* to add record:

  * **Name**: use *xml_id* of the view
  * Check that field **Theme** is set to *Default Theme*
  * Click ``[Save]``

* Click ``[Save]`` at the theme view
* Navigate to ``[[ Website ]] >> Settings``
* Click ``Reload Theme List & Update all websites``
* RESULT: page with the view may be edited independently

Note, that you have to be sure, that each *Website* uses *Default Theme* directly or indirectly (via **Sub-themes** field).

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

* open ``[[ Sales ]] >> Products`` and create product per each company if they don't exist. If a product doesn't belong to any company (i.e. "Company" field is empty), this product will be available on each website you created.
* open HOST1/shop, make order, open backend -- created order belongs to COMPANY1
* open HOST2/shop, make order, open backend -- created order belongs to COMPANY2

Multi-payment
-------------

Note that you are able to use different payment acquiers per each company.

E.g. to use different Paypal accounts for different websites you need to make the following steps:

* go to ``[[ Invoicing ]] >> Configuration >> Payments Acquirers``
* open Paypal acquirer and duplicate it by clicking ``[Action] -> Duplicate``
* for the first one set Company 1, for the second - Company 2
* specify the credentials provided for each acquirer:

  * **Paypal Email ID**
  * **Paypal Merchant ID**
  * **Paypal PDT Token**

Follow the `instruction <https://www.odoo.com/documentation/user/11.0/ecommerce/shopper_experience/paypal.html>`__ to know how to configure Paypal account and get Paypal Identity Token
