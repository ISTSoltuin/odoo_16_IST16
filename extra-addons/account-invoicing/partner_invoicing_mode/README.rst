======================
Partner Invoicing Mode
======================

.. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Faccount--invoicing-lightgray.png?logo=github
    :target: https://github.com/OCA/account-invoicing/tree/16.0/partner_invoicing_mode
    :alt: OCA/account-invoicing
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/account-invoicing-16-0/account-invoicing-16-0-partner_invoicing_mode
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runbot-Try%20me-875A7B.png
    :target: https://runbot.odoo-community.org/runbot/95/16.0
    :alt: Try me on Runbot

|badge1| |badge2| |badge3| |badge4| |badge5| 

This is a base module for implementing different invoicing mode for customers.
It adds a selection field `invoicing_mode` in the Accounting tab of the partner
with a default value (Odoo standard invoicing mode).
But it serves no purpose installed on its own.

The following modules use it to install specific invoicing mode :

    * `partner_invoicing_mode_at_shipping`
    * `partner_invoicing_mode_monthly`

**Table of contents**

.. contents::
   :local:

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/account-invoicing/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OCA/account-invoicing/issues/new?body=module:%20partner_invoicing_mode%0Aversion:%2016.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Camptocamp

Contributors
~~~~~~~~~~~~

* `Camptocamp <https://www.camptocamp.com>`_:

    * Thierry Ducrest <thierry.ducrest@camptocamp.com>

* Phuc (Tran Thanh) <phuc@trobz.com>

Other credits
~~~~~~~~~~~~~

The development of this module has been financially supported by:

* Camptocamp

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/account-invoicing <https://github.com/OCA/account-invoicing/tree/16.0/partner_invoicing_mode>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
