{
    'name': 'Evolution Integration',
    'version': '16.0.0.0',
    'category': 'Tools',
    'summary': 'Integrate Odoo messages with WhatsApp using Evolution API and WebSockets',
    'description': """
This module integrates the Odoo messaging system with WhatsApp using the Evolution API. 
It utilizes WebSockets for real-time communication to send and receive messages.
    """,
    'author': 'Alexandre Santos',
    'website': 'https://odoocast.com',
    'depends': [
        'mail',
    ],
    'data': [
        # Adicione aqui as views, se necessário
        'views/evolution_message_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'evolution_integration/static/src/css/evolution_message.css',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
