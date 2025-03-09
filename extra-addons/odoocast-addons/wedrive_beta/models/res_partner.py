from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    plate = fields.Char(
        string='Placa', 
        help='Placa do veículo'
    )
    
    vehicle_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Veículo',
        help='Veículo associado ao cliente'
    )