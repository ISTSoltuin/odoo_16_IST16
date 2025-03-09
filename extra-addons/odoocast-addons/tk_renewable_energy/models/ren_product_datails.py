# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_solar_product = fields.Boolean(string="Is Solar Product")
    max_power_voltage = fields.Char(string="Max Power Voltage")
    max_power_current = fields.Char(string="Max Power Current")
    temp_coefficient_pmex = fields.Char(string="Pmax")
    temp_coefficient_voc = fields.Char(string="Voc")
    temp_coefficient_isc = fields.Char(string="Isc")
    operating_temp = fields.Char(string="Operating Temp")
    inverter_capacity = fields.Char(string="Inverter Capacity")
    battery_capacity = fields.Char(string="Battery Capacity")
    module_capacity = fields.Char(string="Module Capacity")

