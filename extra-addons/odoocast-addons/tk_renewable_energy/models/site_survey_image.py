# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class SiteSurveyImage(models.Model):
    """Site Survey Image"""
    _name = "site.survey.image"
    _description = __doc__
    _rec_name = 'title'

    title = fields.Char(string="Title", required=True)
    avatar = fields.Binary(string="Avatar", required=True)
    renewable_energy_order_id = fields.Many2one('renewable.energy.order')


