# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class FandiWebhookSimulation(models.Model):
    _name = 'fandi.webhook.simulation'
    _description = 'FandiWebhookSimulation'
    _inherit = 'fandi.webhook.mixin'

    name = fields.Char('Name')
    fandi_client_id = fields.Many2one('fandi.webhook.client', 'Fandi Client')
    fandi_config_id = fields.Many2one('fandi.webhook.config', 'Fandi Config')
    entrance_value = fields.Float('Entrance Value', (16, 2))
    installment_qty = fields.Integer('Installment Qty')
