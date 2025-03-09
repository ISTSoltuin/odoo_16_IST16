from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class CrmLeadLost(models.TransientModel):
    _inherit = 'crm.lead.lost'

    note = fields.Text(string='Brief Note')

    def action_lost_reason_apply(self):
        res = super(CrmLeadLost, self).action_lost_reason_apply()
        for rec in self:
            crm_lead_id = self.env['crm.lead'].browse(self._context.get('active_id'))
            crm_lead_id.sudo().write({
                'lost_reason_id': rec.lost_reason_id,
                'lost_feedback': rec.note
            })
        return res
