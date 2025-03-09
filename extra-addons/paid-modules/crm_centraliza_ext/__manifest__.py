# -*- coding: utf-8 -*-
{
    'name': "Centraliza CRM",

    'summary': """
        personalizar pontos  do crm""",

    'description': """
        person on crm
    """,

    'author': "Alexandre Santos",
    'website': "http://www.odoocast.com",

    
    'category': 'Uncategorized',
    'version': '16.0.0',


    'depends': ['base', 'crm', 'base_import'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/custom_crm_lead_view.xml',
        # 'views/create_sales_pipeline_wizard.xml',
        # 'views/sales_pipeline_view.xml'
        'views/crm_funnel_group_actions.xml',
        'views/crm_team_tree_custom.xml',
        'views/crm_team_form_custom.xml',
        'views/crm_funnel_group_views.xml',
        'views/crm_funnel_group_menus.xml',
        'views/custom_crm_stage_view.xml',

    ],
    'installable': True
    
}

