from odoo import http
from odoo.http import request
import json

class WebhookController(http.Controller):

    @http.route('/webhook/instance', auth='public', methods=['POST'], csrf=False)
    def handle_webhook(self, **kwargs):
        payload = json.loads(request.httprequest.data)
        # Process the webhook payload here
        return "Webhook received"
