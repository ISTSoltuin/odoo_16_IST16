{
    'name': 'Fleet Vehicle Sales',
    'version': '1.0',
    'category': 'Fleet',
    'summary': 'Extend Fleet module to sell vehicles as products',
    'depends': ['fleet', 'sale', 'stock', 'base'],
    "data": [
        "security/ir.model.access.csv",
        "views/fleet_vehicle_views.xml",
        "views/fleet_mercados_views.xml",
        "views/fleet_vehicle_model_server_action.xml",
        "views/product_product_views.xml"
    ],
}
