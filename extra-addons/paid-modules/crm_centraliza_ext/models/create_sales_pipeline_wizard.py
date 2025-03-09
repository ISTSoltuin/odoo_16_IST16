from odoo import api, fields, models

class CreateSalesPipelineWizard(models.TransientModel):
    _name = 'create.sales.pipeline.wizard'
    _description = 'Wizard para criar Sales Pipeline'

    name = fields.Char(string='Nome', required=True)
    is_group = fields.Boolean(string='É Grupo de Funis')
    funnel_ids = fields.Many2many('sales.pipeline', string='Funis no Grupo')

    def create_sales_pipeline(self):
        pipeline_vals = {'name': self.name, 'is_group': self.is_group}

        if self.is_group:
            group = self.env['sales.pipeline'].create(pipeline_vals)
            group.write({'funnel_ids': [(6, 0, self.funnel_ids.ids)]})
        else:
            self.env['sales.pipeline'].create(pipeline_vals)

        return True
