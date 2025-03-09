from odoo import fields, models, api

class ProjectTask(models.Model):
    _inherit = "project.task"
    
    template_id = fields.Many2one(
        comodel_name="project.task.template",
        string="Template model for Task"
    )