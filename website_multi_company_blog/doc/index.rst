=====================================
 Real Multi Website (blog extension)
=====================================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

* Create and configure websites according to the `website_multi_company <https://apps.odoo.com/apps/modules/10.0/website_multi_company/>`__ module documentation
* Open menu ``[[ Website Admin ]] >> Blog >> Blogs``
* Select at **Allowed Websites** field the websites your blog will be available on (leave empty if you wish to post the blog on each website)
* Open menu ``[[ Website Admin ]] >> Configuration >> Website Menus``
* Make sure that there is a menu to open the blog, otherwise create a new one

Usage
=====

* Open your blog on website
* Change URL so it would lead to this blog from your another website - just change website-related part of the URL leaving the same blog-related part
* Since your blog shouldn't be used from your another website, you should see a page with ``403: Forbidden`` on it
