from odoo import http
from odoo.http import request

class FleetVehicleController(http.Controller):
    @http.route('/fleet/vehicle/consult_plate', type='json', auth='user')
    def consult_plate(self, name=str(), cnpj_cpf=str(), phone=str(), plate=str()):
        plate = plate.upper().replace('-', '').replace(' ', '')
        cnpj_cpf = cnpj_cpf.replace('.', '').replace('-', '').replace('/', '')
        
        partner_id = self.get_partner_id(name, cnpj_cpf, phone)
        
        car_id = self.get_car_id(plate, partner_id)
        
        if car_id and partner_id:
            vehicle_id = car_id.vehicle_id
            vehicle_id.driver_id = partner_id
            return {
                'status': 'success',
                'message': 'Veículo registrado no banco de dados',
                'vehicle_id': vehicle_id.name,
                'model': vehicle_id.model_id.name,
                'owner': vehicle_id.driver_id or '',
            }
        elif car_id:
            return {
                'status': 'success',
                'message': 'Veículo existente no banco de dados',
                'vehicle_id': car_id.id,
                'model': car_id.vehicle_id.model_id.name,
                'partner': car_id.vehicle_id.driver_id or '',
            }
        else:
            return {
                'status': 'error',
                'message': 'Veículo não existente no banco de dados, favor criar cadastro manualmente',
            }

    def get_partner_id(self, name, cnpj_cpf, phone):
        partner_id = request.env['res.partner'].search([('cnpj_cpf', '=', cnpj_cpf)], limit=1)
        if not partner_id and cnpj_cpf:
            name = str(name).capitalize()
            partner_id = request.env['res.partner'].create({
                'name': name,
                'cnpj_cpf': cnpj_cpf,
                'phone': phone,
            })
        return partner_id

    def get_car_id(self, plate, partner_id):
        car_id = request.env['car.car'].search([('plate', '=', plate)], limit=1)        
        if not car_id and plate and partner_id:
            car_id = request.env['car.car'].create({
                'plate': plate,
                'partner_id': partner_id.id,
            })
            car_id.action_get_plate_info()
        return car_id