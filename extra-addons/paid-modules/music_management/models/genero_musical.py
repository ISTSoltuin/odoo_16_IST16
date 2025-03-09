from odoo import fields, models, api

class GeneroMusical(models.Model):
    _name = 'genero.musical'
    _description = 'Genero musical'
    
    name = fields.Char(string="Nome do Gênero Musical", required=True)
    # musica_id = fields.One2many(comodel_name="", inverse_name="", string="Musicas deste Gênero")