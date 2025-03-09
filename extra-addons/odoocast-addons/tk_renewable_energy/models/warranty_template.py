# -*- coding: utf-8 -*-
# Copyright 2022-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class WarrantyTemplate(models.Model):
    """Waranty Template"""
    _name = 'warranty.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = __doc__
    _rec_name = 'title'

    title = fields.Char(string="Title", required=True)
    warranty_covered = fields.Html(string="Warranty Covered")
    warranty_not_covered = fields.Html(string="Warranty Not Covered")
