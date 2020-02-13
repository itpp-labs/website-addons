====================================
 Real Multi Website (CRM extension)
====================================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Usage
=====

Lead Creation
-------------

* Make a form on a website or just open ``/contactus`` page
* Fill and submit the form
* Login to backend and open just created lead via menu ``[[ CRM ]] >> Pipeline >> Pipeline``
* RESULT:  the lead has proper **From Website** and **Company** values

Switching websites in backend
-----------------------------

If you have several Websites with the same company, you can filter Leads by Website

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Open menu ``[[ Settings ]] >> Users & Companies >> Users
* Switch to your user
* Click ``[Edit]``
* Activate **Multi Websites for Backend** access right
* Add Websites to **Allowed Websites**
* Click ``[Save]``
* Refresh page in browser (F5)
* Go to ``[[ CRM ]] >> Pipeline >> Pipeline``
* There is a *Website Switcher* in top-right hand corner
* RESULT: Once you change Website lead from other Websites are filtered out

Note: it doesn't work Superuser (Administrator, ID 1), because access rule are not applied for him.
