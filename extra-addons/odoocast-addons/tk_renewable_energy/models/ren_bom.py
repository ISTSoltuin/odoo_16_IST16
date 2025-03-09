# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class RenBom(models.Model):
    """Ren Bom"""
    _name = 'ren.bom'
    _description = __doc__
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    product_qty = fields.Float(string="Quantity")
    renewable_energy_order_id = fields.Many2one('renewable.energy.order')
