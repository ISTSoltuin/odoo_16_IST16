=========
mdfe spec
=========

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:14098f3206cde0cfb2cc546314ab0542a24b8feab63c89655a729df142cae517
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Alpha-red.png
    :target: https://odoo-community.org/page/development-status
    :alt: Alpha
.. |badge2| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fl10n--brazil-lightgray.png?logo=github
    :target: https://github.com/OCA/l10n-brazil/tree/16.0/l10n_br_mdfe_spec
    :alt: OCA/l10n-brazil
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/l10n-brazil-16-0/l10n-brazil-16-0-l10n_br_mdfe_spec
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/l10n-brazil&target_branch=16.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

Este módulo contem a estrutura de dados do ​Manifesto Eletrônico de
Documentos Fiscais (MDF-e). Este módulo não faz nada sozinho, ele
precisaria de um modulo l10n_br_mdfe que mapearia esses mixins nos
documentos fiscais Odoo de forma semlhante a forma como o módulo
l10n_br_nfe faz como o módulo l10n_br_nfe_spec.

Este módulo inclui os leiautes persistantes dos modos de transporte do
MDF-e:

- modo aéreo
- modo aquaviário
- modo ferroviário
- modo rodoviário

Geração
-------

O código dos mixins Odoo desse módulo é 100% gerado a partir dos últimos
esquemas xsd da Fazenda usando xsdata e essa extensão dele:

https://github.com/akretion/xsdata-odoo

O comando usado foi:

export XSDATA_SCHEMA=mdfe; export XSDATA_VERSION=30; export
XSDATA_LANG="portuguese"

xsdata generate nfelib/mdfe/schemas/v3_0 --package nfelib.mdfe.odoo.v3_0
--output=odoo

.. IMPORTANT::
   This is an alpha version, the data model and design can change at any time without warning.
   Only for development or testing purpose, do not use in production.
   `More details on development status <https://odoo-community.org/page/development-status>`_

**Table of contents**

.. contents::
   :local:

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/l10n-brazil/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/l10n-brazil/issues/new?body=module:%20l10n_br_mdfe_spec%0Aversion:%2016.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* Akretion

Contributors
------------

- Raphaël Valyi <raphael.valyi@akretion.com.br>

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-rvalyi| image:: https://github.com/rvalyi.png?size=40px
    :target: https://github.com/rvalyi
    :alt: rvalyi

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-rvalyi| 

This module is part of the `OCA/l10n-brazil <https://github.com/OCA/l10n-brazil/tree/16.0/l10n_br_mdfe_spec>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
