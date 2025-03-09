{
    'name': 'Custom Project Utils',
    'version': '16.0',
    'description': 'Utils for Projects App',
    'summary': 'Utils for Projects',
    'author': 'Isaachintosh / Odoocast',
    'website': 'odoocast.com.br',
    'license': 'LGPL-3',
    'category': 'tools',
    'depends': [
        'base','project','custom_crm_project'
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task_template_views.xml",
        "data/ir_model_data.xml"
    ],
    'auto_install': False,
    'application': False,
}