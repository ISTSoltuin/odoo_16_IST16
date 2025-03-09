# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    fleet_vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Veículo na Frota",
        help="Veículo associado ao produto, na frota",
        ondelete="cascade"
    )
