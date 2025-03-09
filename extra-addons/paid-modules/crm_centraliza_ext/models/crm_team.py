from odoo import models, fields

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    is_funnel_group = fields.Boolean(string="Grupo de Funis?")
    funnel_groups = fields.Many2many('crm.funil.grupo', string="Grupo")


def open_custom_import_view(self):
        return {
            'name': 'Importar Registros (Custom)',
            'type': 'ir.actions.act_window',
            'res_model': 'base_import.import',
            'view_mode': 'form',
            'view_id': self.env.ref('base_import.import_form').id,
            'target': 'new',
        }