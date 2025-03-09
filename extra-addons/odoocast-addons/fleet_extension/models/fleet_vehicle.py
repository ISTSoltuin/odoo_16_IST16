from odoo import models, fields, api
from odoo.exceptions import UserError

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    available_for_sale = fields.Selection(
        [('yes', 'Sim'), ('no', 'Não')],
        string='Disponível para venda'
    )
    
    id_catalogo = fields.Char(string="ID do Catálogo")
    zero_km = fields.Boolean( string="Zero KM", default=False)
    codigo_parceiro = fields.Char(string="Código do Parceiro")
    chassi = fields.Char(string="Chassi")
    manufactured_year = fields.Char(string="Ano de Fabricação")

    sale_value = fields.Float(string='Valor de Venda')
    maintenance_cost = fields.Float(string='Valor de Manutenção')
    documentation_cost = fields.Float(string='Valor de Documentação')
    molicar = fields.Char(string='Molicar')
    mercado_id = fields.Many2one('fleet.mercados', string="Mercado")  
    modelo_related = fields.Char(related='mercado_id.modelo', string="ve", store=True)
    
    catalogo_mercado_1 = fields.Char(related='model_id.catalogo_mercado_1', store=True)
    catalogo_mercado_2 = fields.Char(related='model_id.catalogo_mercado_2', store=True)
    ano_fabricacao = fields.Integer(string="Ano Fabricação")
    versao = fields.Char(string="Versão", store=True)
    vehicle_type = fields.Selection([
        ('automovel', 'AUTOMOVEL'), 
        ('motocicleta', 'MOTOCICLETA'), 
        ('utilitario', 'UTILITARIO'),
        ('car', 'CARRO')
    ], default='automovel', required=True)
    
    @api.depends('model_id')
    @api.onchange('model_id')
    def compute_car_version_id(self):
        for record in self:
            if record.model_id.versao:
                record.versao = record.model_id.versao

    @api.model
    def create(self, vals):
        vehicle = super(FleetVehicle, self).create(vals)
        if vals.get('available_for_sale') == 'yes':
            vehicle._convert_to_product()
        return vehicle

    def write(self, vals):
        res = super(FleetVehicle, self).write(vals)
        for vehicle in self:
            if 'available_for_sale' in vals and vals.get('available_for_sale') == 'yes':
                vehicle._convert_to_product()
        return res

    def _convert_to_product(self):
        message = ""
        molicar = self.molicar or self.id_catalogo or self.catalogo_mercado_1
        if not molicar:
            message = "Código de Integração não encontrado para o veículo.\n"
        if not self.codigo_parceiro:
            message += "Código Parceiro não encontrado para o veículo.\n"
        if not self.chassi:
            message += "Chassi não encontrado para o veículo.\n"
        if not self.ano_fabricacao:
            message += "Ano de fabricação não encontrado para o veículo.\n"
        if not self.model_year:
            message += "Ano do modelo não encontrado para o veículo.\n"
        if not self.sale_value:
            message += "Valor do veículo não encontrado.\n"
        if message:
            message += "Favor revisar antes de prosseguir."
            raise UserError(f"Não foi possível completar a disponibilização\n Erro(s):\n{message}")
        product_vals = {
            'name': self.name,
            'type': 'product',
            'standard_price':self.net_car_value, 
            'list_price': self.sale_value,  # Use sale_value para o preço do produto
            'default_code': self.license_plate,
            'fleet_vehicle_id': self.id,  # Adiciona o ID do veículo ao produto
        }
        product = self.env['product.product'].create(product_vals)

        # Adicionar o produto ao estoque com quantidade 1
        stock_location = self.env.ref('stock.stock_location_stock')
        inventory_adjustment = self.env['stock.quant'].sudo().create({
            'product_id': product.id,
            'location_id': stock_location.id,
            'quantity': 1,
            'company_id': self.env.company.id
        })

        self.message_post(body="Vehicle converted to product")
