{
    'name': 'wedrive_beta',
    'version': '16.0.0.0.0.1',
    'license': 'LGPL-3',
    'summary': 'Módulo para gerenciar prontuário de veículos,baseado no fleet',
    'category': 'Fleet',
    
    'depends': [
        'fleet',
        'base',
        'product',
        'fleet_car_workshop',
        'point_of_sale',
        'l10n_br_base'
    ],
    "data": [
        "views/product_product_views.xml",
        "wizard/create_service_wizard.xml",
        "views/car_car.xml",
        "security/ir.model.access.csv",
        "views/res_company_view.xml",
    ],
    'assets': {
        'point_of_sale.assets': [
            'wedrive_beta/static/src/js/WeDrivePlateSearch.js',
            'wedrive_beta/static/src/js/WeDrivePlateSearchPopup.js',
            'wedrive_beta/static/src/xml/WeDrivePlateSearch.xml',
            'wedrive_beta/static/src/xml/WeDrivePlateSearchPopup.xml',
            'wedrive_beta/static/src/css/wedrive_plate_search_popup.css',
        ],
    },

    'author': 'Alexandre Santos / Isaac Mello (Isaachintosh)',
    'website': 'www.wedrive.com.br',


    'installable': True,
    'application': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png',
        'static/description/icon_menu.png',
    ],
}
