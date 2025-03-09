from odoo import models, fields, api

class FleetMercados(models.Model):
    _name = 'fleet.mercados'
    _description = 'Mercados de Veículos'

    tipo = fields.Char(string="Tipo")
    porte = fields.Char(string="Porte")
    molicar = fields.Char(string="Molicar")
    fipe = fields.Char(string="Fipe")
    marca = fields.Char(string="Marca")
    familia = fields.Char(string="Família")
    modelo = fields.Char(string="Modelo")
    combustivel = fields.Char(string="Combustível")
    cavalos = fields.Integer(string="Cavalos")
    postas = fields.Integer(string="Postas")
    inicio = fields.Integer(string="Início")
    fim = fields.Integer(string="Fim")
    

    @api.model
    def create(self, vals):
        record = super(FleetMercados, self).create(vals)

        brand = self.env['fleet.vehicle.model.brand'].search([('name', '=', record.marca)], limit=1)
        if not brand:
            brand = self.env['fleet.vehicle.model.brand'].create({'name': record.marca})

        # Criar um modelo e associar a versão
        self.env['fleet.vehicle.model'].create({
            'vehicle_type': "automovel",
            'catalogo_mercado_1': record.molicar.replace('-', '').strip() if record.molicar else '',
            'catalogo_mercado_2': record.fipe.replace('-', '').strip() if record.fipe else '',
            'brand_id': brand.id,
            'name': record.familia,
            'versao': record.modelo,  # Preenchendo o campo versao com modelo do mercado
        })

        return record
