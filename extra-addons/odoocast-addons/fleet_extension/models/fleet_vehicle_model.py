from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class FleetVehicleModel(models.Model):
    _inherit = 'fleet.vehicle.model'

    vehicle_type = fields.Selection([
        ('automovel', 'AUTOMOVEL'), 
        ('motocicleta', 'MOTOCICLETA'), 
        ('utilitario', 'UTILITARIO'),
        ('car', 'CARRO')
    ], default='automovel', required=True)

    catalogo_mercado_1 = fields.Char(string="Catálogo Mercado 1", store=True)
    catalogo_mercado_2 = fields.Char(string="Catálogo Mercado 2", store=True)
    versao = fields.Char(string="Versão")

    @api.depends('versao')
    @api.onchange('versao')
    def onchange_name(self):
        index = 1
        for record in self:
            if record.name and record.versao:
                name = record.name.split('-')
                record.name = f"{name[0]}-{record.versao}"
                _logger.info(f"index: {index}/{len(self._ids)} - Name updated to: {record.name}")
                index += 1