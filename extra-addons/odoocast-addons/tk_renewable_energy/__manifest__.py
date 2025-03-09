# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
{
    'name': "Solar Energy Management | Renewable Energy",
    'version': "16.0",
    'description': """Solar & Renewable Energy Management""",
    'summary': "Solar & Renewable Energy Management",
    'author': 'TechKhedut Inc.',
    'website': "https://techkhedut.com",
    'depends': ['base', 'web', 'project', 'sale_management', 'mrp', 'sale_project'],
    'data': [
        # data
        'data/sequence_views.xml',
        'data/solar_energy_product.xml',
        # Security
        'security/ir.model.access.csv',
        'security/groups.xml',
        # Views
        # 'views/assets.xml',
        'views/ren_lead_views.xml',
        'views/ren_product_details_views.xml',
        'views/renewable_energy_order_views.xml',
        'views/ren_quotation_views.xml',
        'views/ren_survey_document_views.xml',
        'views/site_survey_image_views.xml',
        'views/survey_team_views.xml',
        'views/ren_bom_views.xml',
        'views/project_installation_team_views.xml',
        'views/mrp_bom_inherit_views.xml',
        'views/qa_team_views.xml',
        'views/warranty_template_views.xml',
        'views/mrp_production_inherit_views.xml',
        'views/project_task_inherit_views.xml',
        'report/project_material_report_views.xml',
        # Menus
        'views/menus.xml',
    ],
    'qweb': [
        "static/src/xml/template.xml",
    ],
    'images': ['static/description/cover.png'],
    'price': 200,
    'currency': 'EUR',
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
