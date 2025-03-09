# Copyright @ODOOCAST 2024 contato@odoocast.com.br
# Licensed under the AGPL-v3, see the licence;

from odoo import models, fields, api

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    generate_project = fields.Boolean(
        string="Generate Project from Won Stage",
        default=False,
    )
    
    privacy_visibility = fields.Selection(
        selection=[
            ('followers', 'Invited internal users'),
            ('employee', 'All internal users'),
            ('portal', 'Invited portal users and all internal users'),
        ],
        default='portal',
        string="Privacy Visibility",
    )
    
    allow_milestone = fields.Boolean(
        string="Allow Milestone",
        default=False,
    )
    
    auto_generate_basic_tasks = fields.Boolean(
        string='Auto Generate Basic Tasks',
        default=False,
        help='Auto Generate Basic Tasks',
    )