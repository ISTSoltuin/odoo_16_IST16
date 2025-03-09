from odoo import models, fields, api

class Stage(models.Model):
    _inherit = "crm.stage"

    funil_id = fields.Many2one('crm.team', string='Funil')


    @api.model
    def create(self, values):
        # Chame o método create da superclasse para criar o estágio
        stage = super(Stage, self).create(values)

        # Se o estágio foi criado dentro do contexto de um funil específico, associe a equipe de vendas do funil ao estágio
        if 'default_funil_id' in self.env.context:
            funil = self.env['crm.team'].browse(self.env.context['default_funil_id'])
            stage.team_id = funil.team_id

        return stage
