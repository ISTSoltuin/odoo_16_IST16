from odoo import http
from odoo.http import request
import json
from datetime import datetime

class WebhookController(http.Controller):

    @http.route('/webhook/instance', auth='public', methods=['POST'], csrf=False)
    def handle_webhook(self, **kwargs):
        payload = json.loads(request.httprequest.data)
        event_type = payload.get('event')

        if event_type == 'MESSAGES_UPSERT':
            messages = payload.get('messages', [])
            for message in messages:
                self.process_message(message)

        return "Webhook received"

    def process_message(self, message):
        """Processa e salva a mensagem recebida no modelo evolution.message."""
        request.env['evolution.message'].sudo().create({
            'message_id': message.get('id'),
            'content': message.get('content'),
            'sender': message.get('from'),
            'timestamp': datetime.fromtimestamp(message.get('timestamp') / 1000.0)
        })
