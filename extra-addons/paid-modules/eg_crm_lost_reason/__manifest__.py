{
    "name": "lost opportunity reason",

    'version': "16.0",

    'category': "CRM",

    "summary": "This app will display lead loss reason in form view",

    'author': 'INKERP',

    'website': 'https://www.INKERP.com/',

    "depends": ['crm'],
    
    "data": [
        "views/crm_lead_form.xml",
        "wizards/crm_lead_lost_reason.xml",

    ],

    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
