from odoo import models, fields, api

class Selo(models.Model):
    _name = 'music.selo'
    _description = 'Selo (Gravadora)'
   

    # Campos específicos do Selo
    nome_selo = fields.Char(string="Nome do Selo", required=True)
    logotipo_selo = fields.Binary(string="Logotipo do Selo")
    endereco = fields.Text(string="Endereço")
    regiao = fields.Char(string="Região")
    # genero_musical = fields.Many2one('music_management.genero', string="Gênero Musical")
    site_oficial = fields.Char(string="Site Oficial")
    apresentacao = fields.Text(string="Apresentação do Selo")
    representante_legal = fields.Char(string="Representante Legal")
    operador_conta = fields.Char(string="Operador da Conta")
    partner_id = fields.Many2one('res.partner', string='Contato Selo')
    genero_musical_ids = fields.Many2many(
        comodel_name="genero.musical",
        string="Gêneros Musicais"
    )