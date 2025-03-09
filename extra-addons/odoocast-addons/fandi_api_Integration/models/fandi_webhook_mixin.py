# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class FandiWebhookMixin(models.Model):
    _name = 'fandi.webhook.mixin'
    _description = 'FandiWebhookMixin'

    name = fields.Char('Name')
    
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)

    api_environment = fields.Selection([
        ('production', 'Production'),
        ('homologation', 'Homologation'),
        ('sandbox', 'Sandbox')
    ], string='API Environment', default='sandbox')
