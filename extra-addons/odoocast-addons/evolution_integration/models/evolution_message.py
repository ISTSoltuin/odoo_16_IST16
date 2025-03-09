from odoo import models, fields, api
import requests

class EvolutionMessage(models.Model):
    _name = 'evolution.message'
    _description = 'Evolution Message'

    message_id = fields.Char(string='Message ID')
    content = fields.Text(string='Content')
    sender = fields.Char(string='Sender')
    phone_number = fields.Char(string='Phone Number')
    timestamp = fields.Datetime(string='Timestamp')

    def send_message(self):
        """Envia uma mensagem usando a Evolution API."""
        url = 'https://api.facillink.com.br/manager/alexandre/send_message'  # Atualizado com o seu URL
        payload = {
            'content': self.content,
            'to': self.phone_number
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
