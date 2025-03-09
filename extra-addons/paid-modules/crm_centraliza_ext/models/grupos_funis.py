from odoo import models, fields

class CrmFunnelGroup(models.Model):
    _name = 'crm.funil.grupo'
    _description = 'CRM Funnel Group'

    name = fields.Char(string='Nome', required=True)
    description = fields.Text(string='Descrição')
    funis_ids = fields.Many2many('crm.team', string='Funis de Vendas')
    # Adicione outros campos conforme necessário
