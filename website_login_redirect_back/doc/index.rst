========================
 Login Page Redirection
========================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

Make sure that you have a user with **User Type**->*Portal*.
if you have demo data installed, there is a portal user with following credentials:

   * Email: ``portal``
   * Password: ``portal``

Or just create a new user with **User Type** -> *Portal*

Usage
=====

* Log out from the website
* Go to any page of your website
* Click the ``[Sing in]`` button
* Log in as a portal user
* RESULT: after successful login, you will be redirected to the page you were on before authentication
