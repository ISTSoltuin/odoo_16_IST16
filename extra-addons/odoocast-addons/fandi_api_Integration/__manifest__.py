{
    'name': 'Simulador de Financiamento',
    'version': '16.0',
    'depends': ['base','website_sale','product','fleet','crm','fleet_extension'],
    "data": [
        "views/product_template_view.xml",
        "views/res_company_views.xml",
        "views/fandi_webhook_call_views.xml",
        "security/ir.model.access.csv",
        "views/fandi_webhook_config_views.xml",
        "views/fandi_webhook_client_views.xml",
        "views/fandi_webhook_simulation_views.xml",
        "views/fandi_webhook_mixin_views.xml"
    ],
    'assets': {
        'web.assets_frontend': [
            '/fandi_api_Integration/static/src/js/simulate_financing.js',
        ],
    },
    'installable': True,
    'application': True,
}

