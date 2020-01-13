==========================
 Event guest Custom Field
==========================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way
* After installation you need to configure each Event. Otherwise there will be no fields at website attendees form.

Configuration
=============

* Open menu ``Event``
* Select or create Event
* At ``Website Fields`` tab update list of fields

Usage
=====

* Open ``/event`` page
* Select desired Event
* Select quantity of tickets and click ``[Order Now]``
* RESULT: specified fields are shown
* Fill the fields and proceed checkout
* Go back to backend. Open menu ``Event``
* Check new attendee(s) of the Event
* Result: Attendee(s) fields are stored in **Contact** record

Email field at the form
=======================

* When email column is presented and there is a partner with that email:

  * if partner has confirmed registration for the event:

    * registration is blocked. Warning is shown

  * if partner has some of fields

    * grey them out with a message "This email address already has an account. Data will be taken from this account"

* Registration form doesn't allow to register two attendees with the same email

* When partner record exists before purchasing the module and current user is not that partner, then new partner's details are posted under registration form as a message. Such cases has to be handled manually, because we cannot update them automatically to partner for security reasons.
