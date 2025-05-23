==========================
Common EDI fiscal features
==========================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:034c56eb0f91badcd72c56e05219d0afaa44bc89fad0779ed5b8a484ecb77884
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fl10n--brazil-lightgray.png?logo=github
    :target: https://github.com/OCA/l10n-brazil/tree/16.0/l10n_br_fiscal_edi
    :alt: OCA/l10n-brazil
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/l10n-brazil-16-0/l10n-brazil-16-0-l10n_br_fiscal_edi
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/l10n-brazil&target_branch=16.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

Este módulo estende o módulo ``l10n_br_fiscal`` e cuida da parte de EDI
(Electronic Data Interchange) que é comum entre os vários documentos
fiscais no Brasil. Ele introduz os modelos de eventos de transmissão, de
correções... Alem disso ele cuida das possíveis transições de estado do
documento fiscal em função dos retornos dos webservices (campo
``state_edoc``).

**Table of contents**

.. contents::
   :local:

Usage
=====

Use os botões na barra de header do documento fiscal para alterar o
estado do documento fiscal, para abrir os wizards e para interagir com a
fazenda... Quando o módulo ``l10n_br_account`` ou alguns módulos de
documentos fiscais específicos como ``l10n_br_nfe`` ou ``l10n_br_nfse``
são instalados, alguns métodos de transição de estado do módulo
``l10n_br_fiscal_edi`` são chamados automaticamente, por exemplo ao
confirmar ou cancelar uma nota.

Known issues / Roadmap
======================

O código deste módulo foi feito antes dos repos ``OCA/edi`` e
``OCA/edi-framework``. O código do ``document_workflow.py`` por exemplo
foi uma espécie de tradução em código do "workflow de state machine" que
tinha sido customizado para a NFe na versão 8.0 mas que teve que ser
re-escrito quando o engine de workflow foi removido na versão 10.0.
Nisso o código deste módulo tem bastante possibilidades de melhorias...

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/l10n-brazil/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/l10n-brazil/issues/new?body=module:%20l10n_br_fiscal_edi%0Aversion:%2016.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* Akretion
* KMEE

Contributors
------------

- `Akretion <https://www.akretion.com/pt-BR>`__:

  - Renato Lima <renato.lima@akretion.com.br>
  - Raphaël Valyi <raphael.valyi@akretion.com.br>

- `KMEE <https://www.kmee.com.br>`__:

  - Luis Felipe Mileo <mileo@kmee.com.br>

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-renatonlima| image:: https://github.com/renatonlima.png?size=40px
    :target: https://github.com/renatonlima
    :alt: renatonlima
.. |maintainer-rvalyi| image:: https://github.com/rvalyi.png?size=40px
    :target: https://github.com/rvalyi
    :alt: rvalyi
.. |maintainer-mileo| image:: https://github.com/mileo.png?size=40px
    :target: https://github.com/mileo
    :alt: mileo

Current `maintainers <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-renatonlima| |maintainer-rvalyi| |maintainer-mileo| 

This module is part of the `OCA/l10n-brazil <https://github.com/OCA/l10n-brazil/tree/16.0/l10n_br_fiscal_edi>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
