# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    vehicle_description = fields.Char('Vehicle Description')
    vehicle_value = fields.Float('Vehicle Value', (16, 2))
    installments = fields.Integer('Installments')
    installment_value = fields.Float('Installment Value', (16, 2))
