# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class RenSurveyDocument(models.Model):
    """REN Survey Document"""
    _name = 'ren.survey.document'
    _description = __doc__
    _rec_name = 'title'

    title = fields.Char(string="Title", required=True)
    file_name = fields.Char(string="filename")
    avatar = fields.Binary(string="Document", required=True)
    renewable_energy_order_id = fields.Many2one('renewable.energy.order')
