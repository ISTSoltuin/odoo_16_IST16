from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"
    
    vehicle_ids = fields.Many2many(
        comodel_name="fleet.vehicle.model",
        relation="product_vehicle_rel",
        column1="product_id",
        column2="vehicle_id",
        string="Veículos"
    )