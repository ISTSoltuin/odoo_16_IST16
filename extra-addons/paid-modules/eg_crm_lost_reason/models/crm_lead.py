from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    lost_reason_id = fields.Many2one(string='Lost Reason')
    lost_feedback = fields.Text(string='Note')
