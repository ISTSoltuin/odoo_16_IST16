from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    sinesp_api_option = fields.Selection([
            ('api_placas', 'API Placas'),
            ('placa_fipe', 'API Placa Fipe'),
            ('disabled', 'Desativado'),
        ], 
        string='Sinesp API Option',
        default='disabled'
    )
    
    api_placas_token = fields.Char(
        string='API Placas Token',
    )