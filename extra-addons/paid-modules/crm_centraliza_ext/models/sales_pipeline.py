from odoo import api, fields, models

class SalesPipeline(models.Model):
    _name = 'sales.pipeline'
    _description = 'Sales Pipeline'

    name = fields.Char(string='Nome', required=True)
    is_group = fields.Boolean(string='É Grupo de Funis')
    funnel_ids = fields.Many2many('sales.pipeline', 'sales_pipeline_group_rel', 'group_id', 'funnel_id', string='Funis no Grupo')

    # Adicione outros campos conforme necessário
