from odoo import fields, models

class CarCar(models.Model):
    _inherit = 'car.car'
    
    vehicle_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Veículo',
        ondelete='cascade',
        help='Veículo associado ao carro.',
        required=False
    )
    
    def create_car_service_tasks(self):
        # Lógica para criar tarefas de serviço relacionadas ao carro
        view_id = self.env.ref('wedrive_beta.create_service_wizard_form')
        if view_id:
            return {
                'name': 'Ordens de Serviço',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'create.service.wizard',
                'view_id': view_id.id,
                'target': 'new',
                'context': {
                    'default_car_id': self.id,
                }
            }

    plate = fields.Char(
        string='Placa', 
        required=True
    )

    def action_get_plate_info(self):
        if self.plate:
            vehicle_obj = self.env['fleet.vehicle']
            vehicle_data = vehicle_obj.action_get_plate_info_json(self.plate)
            if vehicle_data:
                vehicle_id = vehicle_obj.create(vehicle_data)
                self.vehicle_id = vehicle_id