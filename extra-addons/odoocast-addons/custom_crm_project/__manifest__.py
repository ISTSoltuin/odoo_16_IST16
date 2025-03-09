{
    'name': 'Custom CRM Project Integration',
    'version': '16.0',
    'description': 'Custom CRM Project Integration',
    'summary': 'Converts Won Leads into Projects',
    'author': 'Isaachintosh / Odoocast',
    'website': 'odoocast.com.br',
    'license': 'LGPL-3',
    'category': 'tools',
    'depends': [
        'base',
        'crm',
        'project',
        'website',
        'website_crm'
    ],
    "data": [
        "views/crm_stage_views.xml",
        "views/crm_lead_views.xml",
        "views/project_project_views.xml"
    ],
    'auto_install': False,
    'application': False,
}