# -*- coding: utf-8 -*-
{
    'name': "Hyppow Gestao de musica",

    'summary': """
        Permite a Gestao da plataforma de streaming de musica""",

    'description': """
        Gestao plataforma de streaming de musica.  Permite ver os artistas,
        albuns,musicas, numero de visualizacoes,comissoes que o artista ganha por musica.
    """,

    'author': "Alexandre Santos",
    'website': "http://www.odoocast.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/music_management_menu.xml',
        'views/artista_view.xml',
        'views/selo_view.xml',
    ],
    'installable': True
}
