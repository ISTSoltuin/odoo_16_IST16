# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class FandiWebhookCall(models.Model):
    _name = 'fandi.webhook.call'
    _description = 'FandiWebhookCall'
    _inherit = 'fandi.webhook.mixin'

    active = fields.Boolean('Active', default=True)
    name = fields.Char('Name')
    
    fandi_config_id = fields.Many2one('fandi.webhook.config', 'Fandi Config')
    fandi_client_id = fields.Many2one('fandi.webhook.client', 'Fandi Client')
    fandi_webhook_simulation_id = fields.Many2one('fandi.webhook.simulation', 'Fandi Webhook Simulation')
    json_body =  fields.Text('JSON Body')
    json_response = fields.Text('JSON Response')
    
    url_fandi = fields.Char('URL')
    token_acesso = fields.Char('Token')
    
    point_of_sale_id = fields.Integer('Point of Sale ID')
    fandi_company_id = fields.Integer('Fandi Company ID')
    seller_id = fields.Integer('Seller ID')