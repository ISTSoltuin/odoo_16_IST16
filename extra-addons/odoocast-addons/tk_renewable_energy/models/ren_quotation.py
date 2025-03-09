# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class RenQuotation(models.Model):
    """Ren Quotation"""
    _name = 'ren.quotation'
    _description = __doc__
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', string="Product", domain="[('is_solar_product','=',True)]",
                                 required=True)
    description = fields.Char(string="Description", required=True)
    price = fields.Monetary(string="Price")

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', related="company_id.currency_id")
    renewable_energy_order_id = fields.Many2one('renewable.energy.order')

    @api.onchange('product_id', 'price')
    def solar_product_price(self):
        for rec in self:
            if rec.product_id:
                rec.price = rec.product_id.standard_price
