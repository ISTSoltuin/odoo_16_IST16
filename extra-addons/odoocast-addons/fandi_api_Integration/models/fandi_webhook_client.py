# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class FandiWebhookClient(models.Model):
    _name = 'fandi.webhook.client'
    _description = 'FandiWebhookClient'
    _inherit = 'fandi.webhook.mixin'

    name = fields.Char('Name')
    pcd = fields.Boolean('PCD')
    mobile_phone = fields.Char('Mobile Phone')
    gender = fields.Char('Gender')
    birth_date = fields.Date('Birth Date')
    cnh_id_card_number = fields.Char('CNH ID Card Number')
    taxi_usage = fields.Boolean('Taxi Usage')
    cpf = fields.Char('CPF')
    email = fields.Char('Email')
