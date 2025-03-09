# Copyright @ODOOCAST 2024 contato@odoocast.com.br
# Licensed under the AGPL-v3, see the licence;

from odoo import models, fields, api

class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    crm_lead_id = fields.Many2one(
        comodel_name="crm.lead",
        string="CRM Lead"
    )