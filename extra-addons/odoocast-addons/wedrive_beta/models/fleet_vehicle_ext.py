import requests
from odoo import models, fields, api
from odoo.exceptions import ValidationError
# from sinesp_client import SinespClient
from base64 import b64decode, b64encode

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    license_plate = fields.Char(string='License Plate')
    marca = fields.Char(string='Marca')
    modelo = fields.Char(string='Modelo')
    ano = fields.Char(string='Ano')
    cor = fields.Char(string='Cor')
    chassi = fields.Char(string='Chassi')
    municipio = fields.Char(string='Município')
    uf = fields.Char(string='UF')
    segmento = fields.Char(string='Segmento')
    anoModelo = fields.Char(string='Ano do Modelo')
    subsegmento = fields.Char(string='Subsegmento')
    combustivel = fields.Char(string='Combustível')
    cilindradas = fields.Char(string='Cilindradas')
    # incluir campo binário (visivel somente em modo debug) para salvar o json retornaado da api
    # Razão: ser possivel reprocessar os dados da api em caso de erro ou atualização do cadastro
    # api_response = fields.Binary(string='API Response')

    def action_get_plate_info_json(self, plate):
        # Tratamento para uppercase
        plate = plate.upper().replace('-', '').replace(' ', '')
        result = {}
        # if self.env.company.sinesp_api_option == 'sinesp_cidadao':
        #     result = self.action_get_plate_info_sinesp_cidadao(plate)
        if self.env.company.sinesp_api_option == 'placa_fipe':
            result = self.action_get_plate_info_placa_fipe(plate)
        elif self.env.company.sinesp_api_option == 'api_placas':
            result = self.action_get_plate_info_api_placas(plate)
        if result:
            vals = {
                'license_plate': result.get('placa', ''),
                'marca': result.get('marca', ''),
                'modelo': result.get('modelo', ''),
                'ano': result.get('ano', ''),
                'cor': result.get('cor', ''),
                'chassi': result.get('chassi', ''),
                'municipio': result.get('municipio', ''),
                'uf': result.get('uf', ''),
                'segmento': result.get('segmento', ''),
                'anoModelo': result.get('anoModelo', ''),
                'subsegmento': result.get('subsegmento', ''),
                'combustivel': result.get('combustivel', ''),
                'cilindradas': result.get('cilindradas', ''),
            }
            model_id = self.get_model_id(vals, result.get('logo', ''))
            if model_id:
                vals['model_id'] = model_id.id
            return vals

    def get_model_id(self, vals, logo=''):
        marca = vals.get('marca','')
        if marca == "VW":
            marca = "VOLKSWAGEN"
        brand_id = self.env['fleet.vehicle.model.brand'].search([('name', 'ilike', marca)], limit=1)
        if not brand_id:
            brand_id = self.env['fleet.vehicle.model.brand'].create({
                'name': marca,
                'image_128': vals.get('logo', '')
            })
        # TODO: 
        # tratar filtros em um domain condicional baseado no vals, nome do modelo + ano do modelo
        # deve ser possivel ter mais de um modelo com o mesmo nome mas de anos de fabricação diferentes.
        model_id = self.env['fleet.vehicle.model'].search([('name', 'ilike', vals.get('modelo'))], limit=1)
        if not model_id:
            default_fuel_type = 'gasoline'
            if vals.get('combustivel'):
                if 'gas' in vals.get('combustivel').lower():
                    default_fuel_type = 'gasoline'
                elif 'diesel' in vals.get('combustivel').lower():
                    default_fuel_type = 'diesel'
                elif 'gnv' in vals.get('combustivel').lower():
                    default_fuel_type = 'cnv'
                elif 'elétrico' in vals.get('combustivel').lower():
                    default_fuel_type = 'electric'

            model_id = self.env['fleet.vehicle.model'].create({
                'name': vals.get('modelo'),
                'model_year': int(vals.get('anoModelo')),
                'brand_id': brand_id.id,
                'vehicle_type': 'car',
                'color': vals.get('cor'),
                'default_fuel_type': default_fuel_type
            })
        return model_id
    
    def action_get_plate_info_api_placas(self, plate):
        # Implementação da API para obter informações da placa
        try:
            token = self.env.company.api_placas_token
            daily_search_count = requests.get(f"https://wdapi2.com.br/saldo/{token}")
            if daily_search_count.status_code == 200:
                if daily_search_count.json()['qtdConsultas'] <= 3:
                    raise ValidationError('Limite de consultas excedido. Aguarde o dia seguinte.')
            url = f"https://wdapi2.com.br/consulta/{plate}/{token}"
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Verifica se houve erro na requisição
            data = response.json()
            if response.status_code == 200:
                json_data = {
                    'marca': data['MARCA'],
                    'modelo': data['MODELO'],
                    'ano': data['ano'],
                    'cor': data['cor'],
                    'chassi': data['extra']['chassi'],
                    'municipio': data['municipio'],
                    'uf': data['extra']['uf_placa'],
                    'segmento': data['extra']['segmento'],
                    'anoModelo': data['extra']['ano_modelo'],
                    'combustivel': data['extra']['combustivel'],
                    'cilindradas': data['extra']['cilindradas'],
                    'placa': data['placa'],
                }
                if data.get('logo'):
                    logo = requests.get(data['logo'])
                    if logo.text:
                        # converte a imagem para base64
                        logo_image = b64encode(logo.content).decode('utf-8')
                        data['logo'] = logo_image
                return json_data
        except Exception as e:
            pass
    
    def action_get_plate_info_sinesp_cidadao(self, plate):
        sc = SinespClient()
        try:
            result = sc.search(plate)
            return result
        except Exception as ex:
            raise ValidationError(ex)
    
    def action_get_plate_info_placa_fipe(self, plate):
        url = "https://api.placafipe.xyz/getplaca"
        token = "1CD78B0C54849E565D2E42FFC2AE899ADD8A401200FA43683D0C42ED76BBAD5F"

        payload = {
            "placa": plate,
            "token": token,
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Verifica se houve erro na requisição
            data = response.json()
            if data.get("codigo") == 1:
                return {
                    'marca': data['informacoes_veiculo']['marca'],
                    'modelo': data['informacoes_veiculo']['modelo'],
                    'ano': data['informacoes_veiculo']['ano'],
                    'cor': data['informacoes_veiculo']['cor'],
                    'chassi': data['informacoes_veiculo']['chassi'],
                    'municipio': data['informacoes_veiculo']['municipio'],
                    'uf': data['informacoes_veiculo']['uf'],
                    'segmento': data['informacoes_veiculo']['segmento'],
                    'anoModelo': data['informacoes_veiculo']['anoModelo'],
                    'subsegmento': data['informacoes_veiculo']['subsegmento'],
                    'combustivel': data['informacoes_veiculo']['combustivel'],
                    'cilindradas': data['informacoes_veiculo']['cilindradas'],
                }
        except requests.exceptions.RequestException as e:
            # Trata erros de conexão, timeouts, etc.
            print(f"Erro na requisição HTTP: {e}")
        except ValueError as e:
            # Trata erros ao decodificar a resposta JSON
            print(f"Erro ao decodificar a resposta JSON: {e}")
        return {}

    @api.model
    def create(self, vals):
        result = super(FleetVehicle, self).create(vals)
        return result
