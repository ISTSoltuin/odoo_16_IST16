from odoo import models, fields, api

class Artista(models.Model):
    _name = 'music.artista'
    _description = 'Artista'
    

    # Campos específicos do Artista
    nome_artista = fields.Char(string="Nome Artístico")
    aniversario = fields.Date(string="Aniversário")
    email = fields.Char(string="Email")
    nome_legal = fields.Char(string="Nome Legal")
    tipo_identidade = fields.Selection([
        ('rg', 'RG'),
        ('cnh', 'CNH'),
        ('passaporte', 'Passaporte')
    ], string="Tipo de Identidade")
    foto_documento = fields.Binary(string="Foto do Documento")
    numero_identidade = fields.Char(string="Número da Identidade")
    partner_id = fields.Many2one('res.partner', string='Contato Artista')

