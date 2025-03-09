from odoo import fields, models

class CreateServiceWizard(models.TransientModel):
    _name = "create.service.wizard"
    _description = "Create Service Wizard"

    service_name = fields.Char(string='Service Name', required=True)
    service_description = fields.Text(string='Service Description')
    # computar valor com base na listagem de serviços / produtos usados
    service_price = fields.Float(string='Service Price', required=True)
    car_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Carro',
        required=True,
    )
    product_ids = fields.Many2many(
        comodel_name='product.product',
        string='Produtos',
        required=True,
    )

    def create_service(self):
        service_vals = {
            'name': self.service_name,
            'description': self.service_description,
            'price': self.service_price,
        }
        self.env['car.workshop'].create(service_vals)