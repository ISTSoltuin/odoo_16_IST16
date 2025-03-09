# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class FandiWebhookConfig(models.Model):
    _name = 'fandi.webhook.config'
    _description = 'FandiWebhookConfig'
    _inherit = 'fandi.webhook.mixin'

    name = fields.Char('Name')
    access_key = fields.Char('Access Key')
    
    cnpj_company = fields.Char('CNPJ Company')
    cpf_seller = fields.Char('CPF Seller')
    
    url_callback = fields.Char('URL Callback')
    redirect_url = fields.Char('Redirect URL')
    
    data_confirmation = fields.Text('Data Confirmation')
    
    url_logo = fields.Char('URL Logo')
    background_color = fields.Char('Background Color')
    highlight_color = fields.Char('Highlight Color')
    highlight_action_button = fields.Char('Highlight Action Button')
    highlight_action_button_text = fields.Char('Highlight Action Button Text')
    
    final_screen_exhibit = fields.Boolean('Exhibit Final Screen')
    final_screen_highlight_message = fields.Boolean('Highlight Message Final Screen')
    allow_change_conditions = fields.Boolean('Allow Change Conditions')
    show_vehicle_value = fields.Boolean('Show Vehicle Value')
    show_screen_complete_registration = fields.Boolean('Show Screen Complete Registration')
