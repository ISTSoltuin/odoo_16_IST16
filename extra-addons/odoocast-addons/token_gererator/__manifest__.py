# fake_token_generator/__manifest__.py

{
    'name': 'Token Generator',
    'version': '1.0',
    'author': 'Aosdevs',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'views/token_view.xml',
    ],
    'installable': True,
    'application': True,
}
