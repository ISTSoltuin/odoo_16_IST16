=======================================
Sales order invoicing grouping criteria
=======================================

.. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Production%2FStable-green.png
    :target: https://odoo-community.org/page/development-status
    :alt: Production/Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Faccount--invoicing-lightgray.png?logo=github
    :target: https://github.com/OCA/account-invoicing/tree/16.0/sale_order_invoicing_grouping_criteria
    :alt: OCA/account-invoicing
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/account-invoicing-16-0/account-invoicing-16-0-sale_order_invoicing_grouping_criteria
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runbot-Try%20me-875A7B.png
    :target: https://runbot.odoo-community.org/runbot/95/16.0
    :alt: Try me on Runbot

|badge1| |badge2| |badge3| |badge4| |badge5| 

This module allows to use custom criteria for grouping sales orders to be
invoiced.

Default criteria for grouping (invoicing partner, company and used currency)
will be always applied, as if not respected, there will be business
inconsistencies, but you can add more fields to split the invoicing according
them.

**Table of contents**

.. contents::
   :local:

Configuration
=============

For creating new grouping criteria:

#. Go to *Invoicing > Configuration > Management > Invoicing Grouping Criteria*.
#. Create or modify existing criteria, selecting fields belonging to "Sales
   Order" header model for grouping according them.
#. Invoicing address and currency will always be applied with the selected
   ones.

For setting a different grouping criteria for a specific customer:

#. Go to *Invoicing > Sales > Master Data > Customers*.
#. Open the desired customer.
#. Go to *Invoicing* page.
#. Set on "Sales Invoicing Grouping Criteria" the desired grouping
   criteria.

For setting a different default grouping criteria than the standard for the
whole company:

#. Go to *Invoicing > Configuration> Settings*.
#. Locate inside "Sales Order Invoicing" section, the field "Default
   Grouping Criteria".
#. Introduce there the grouping criteria to be applied by default. If empty,
   the general default of invoicing address + currency + company will be
   applied.

Usage
=====

#. Go to *Sales > Invoicing > Orders to Invoice*.
#. Select sales orders whose invoicing you want to do.
#. Click on *Action > Invoice Order*.
#. Click on "Create and View Invoices" button.
#. On that moment, the grouping criteria will be applied, and you will see
   different invoices if the criteria doesn't match for them.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/account-invoicing/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OCA/account-invoicing/issues/new?body=module:%20sale_order_invoicing_grouping_criteria%0Aversion:%2016.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Tecnativa

Contributors
~~~~~~~~~~~~

* `Tecnativa <https://www.tecnativa.com>`__:

  * Pedro M. Baeza

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-pedrobaeza| image:: https://github.com/pedrobaeza.png?size=40px
    :target: https://github.com/pedrobaeza
    :alt: pedrobaeza

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-pedrobaeza| 

This module is part of the `OCA/account-invoicing <https://github.com/OCA/account-invoicing/tree/16.0/sale_order_invoicing_grouping_criteria>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
