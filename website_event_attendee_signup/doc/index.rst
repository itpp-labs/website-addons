==========================
 Auto Sign Up Event guest
==========================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

* At ``Events`` menu create or select existing event
* Switch **[x] Signup attendees to portal** on
* Switch **[x] Create Partners in registration** on
* At ``Email Schedule`` add a line:

  * **Email to Send**:  *Event: Signup*
  * **Unit**: *Immediately*
  * **When to Run**: *After each registration*

Alternative email template configuration:

* `Activate Developer Mode <https://odoo-development.readthedocs.io/en/latest/odoo/usage/debug-mode.html>`__
* Open menu ``[[ Settings ]] >> Technical >> Email >> Templates``
* Filter out records by keyword *Event*
* Open *Event: Signup* record
* Click ``[Edit]``
* Click icon ``</>`` to switch to Code view
* Copy the code related to signup
* Go back to templates
* Open *Event: Reminder* record
* Click ``[Edit]``
* Click icon ``</>`` to switch to Code view
* Paste the copied code
* Click ``[Save]``

Usage
=====

* Register few attendees to the Event via Website (``/event`` page)
* Confirm the registrations (e.g. via backend)
* RESULT: every attendees receives email with a link to signup to portal
