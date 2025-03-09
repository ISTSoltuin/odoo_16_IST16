from odoo import fields, models, api
import json, requests
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_form_visible = fields.Boolean(
        string="Exibir formulário de simulação",
        default=False
    )
    
    @api.model
    def enviar_simulacao(self, name, cpf, telefone, product_id):
        # Captura as informações do cliente e do produto (veículo)
        cliente_data = {
            "nome": name,
            "cpf": cpf,
            "telefone": telefone,
            "sexo": "M",
            "dataNascimento": "1977-10-26",
            "possuiCnh": True,
            "usoTaxi": False,
            "pcd": False,
            "email": "email@email.com",
        }

        # Captura as informações do veículo a partir do ID do product.template
        veiculo_data = self.get_vehicle_data(product_id)

        if 'has_error' in veiculo_data and veiculo_data.get('has_error'):
            return {'success': False, 'message': veiculo_data.get('message')}
        
        # Chamada para a API para obter o GUID
        guid = self.obter_guid(cliente_data, veiculo_data)
        if not guid or 'status_code' in guid:
            message = guid.get('content') or guid.get('text') or guid.get('message')
            return {
                'success': False,
                'message': message
            }

        # Simulação de financiamento com base nas informações capturadas
        molicar = str(veiculo_data['molicar'])
        if molicar:
            molicar = molicar.replace('-', '')
            veiculo_data['molicar'] = molicar
            
        sim_result = self.simular_financiamento(guid, cliente_data, veiculo_data)

        if sim_result and 'error' not in sim_result:
            # Criação do card no CRM
            self.create_crm_lead(cliente_data, veiculo_data, sim_result)

            # Retorna as parcelas e valores para o frontend
            vals = {
                'success': True,
            }
            if sim_result.get('valorParcela'):
                vals.update({'valor_parcela': sim_result.get('valorParcela')})
            if sim_result.get('quantidadeParcelas'):
                vals.update({'quantidade_parcelas': sim_result.get('quantidadeParcelas')})
            if sim_result.get('valorEntrada'):
                vals.update({'valor_entrada': sim_result.get('valorEntrada')})
            if sim_result.get('valorFinanciado'):
                vals.update({'valor_financiado': sim_result.get('valorFinanciado')})
            if sim_result.get('veiculo') and sim_result.get('veiculo').get('fabricante'):
                vals.update({'fabricante': sim_result.get('fabricante')})
            if sim_result.get('veiculo') and sim_result.get('veiculo').get('familia'):
                vals.update({'familia': sim_result.get('veiculo').get('familia')})
            if guid.get('config') and guid.get('config').get('linkRedirecionamento'):
                vals.update({'link_redirecionamento': guid.get('config').get('linkRedirecionamento')})
            if sim_result.get('valorTotal'):
                vals.update({'valor_total': sim_result.get('valorTotal')})
            if veiculo_data.get('valor'):
                vals.update({'valor_veiculo': veiculo_data.get('valor')})
            return vals

        else:
            return {
                'success': False,
                'message': f"Erro na simulação {sim_result.get('error')}\n{sim_result.get('message')}"
            }

    def get_vehicle_data(self, product_id):
        has_error = False
        # Buscando as informações no modelo product.template
        product = self.env['product.product'].browse(int(product_id))
        placa = product.name.split('/')[-1]  # Supondo que a placa é o último elemento
        fleet_vehicle_id = self.env['fleet.vehicle'].search([('license_plate','=', placa)], limit=1)
        if not fleet_vehicle_id:
            fleet_vehicle_id = product.fleet_vehicle_id
        
        valor_veiculo = fleet_vehicle_id.sale_value or product.list_price

        # Estrutura de dados do veículo que será enviado para a API
        molicar = fleet_vehicle_id.molicar or fleet_vehicle_id.id_catalogo or fleet_vehicle_id.catalogo_mercado_1
        message = ""
        if not molicar:
            message = "Código de Integração não encontrado para o veículo.\n"
        if not fleet_vehicle_id.ano_fabricacao:
            message += "Ano de fabricação não encontrado para o veículo.\n"
        if not fleet_vehicle_id.model_year:
            message += "Ano do modelo não encontrado para o veículo.\n"
        if message:
            has_error = True
            return {
                'has_error': has_error,
                'message': message
            }
        else:
            return {
                "molicar": molicar,
                "zeroKm": fleet_vehicle_id.zero_km,
                "codigoParceiro": fleet_vehicle_id.codigo_parceiro or "",
                "chassi": fleet_vehicle_id.chassi or "",
                "anoFabricacao": int(fleet_vehicle_id.ano_fabricacao),
                "anoModelo": int(fleet_vehicle_id.model_year),
                "valor": int(valor_veiculo)
            }

    def get_config_data(self, token):
        cnpj_loja = self.env.company.cnpj_loja.replace('.','').replace('/','').replace('-','')
        cpf_vendedor = self.env.company.cpf_vendedor or ""
        url_logomarca = self.env.company.url_logomarca
        cor_fundo = self.env.company.cor_fundo
        cor_destaque = self.env.company.cor_destaque
        cor_fonte_botao = self.env.company.cor_fonte_botao
        url_callback = self.env.company.url_callback
        return {
            "chaveAcesso": token,
            "cnpjLoja": cnpj_loja,
            "cpfVendedor": cpf_vendedor or "",
            "urlLogomarca": url_logomarca,
            "corFundo": cor_fundo,
            "corDestaque": cor_destaque,
            "corFonteBotao": cor_fonte_botao,
            "urlCallback": url_callback
        }

    def obter_guid(self, cliente_data, veiculo_data):
        # Implementação da chamada para obter o GUID
        api_environment = self.env.company.api_environment
        
        if api_environment == 'production':
            url = self.env.company.production_webhook_url
            token = self.env.company.production_token
        elif api_environment == 'homologation':
            url = self.env.company.homologation_webhook_url
            token = self.env.company.homologation_token
        else:
            url = self.env.company.sandbox_webhook_url
            token = self.env.company.sandbox_token
        
        if not url:
            raise ValueError(f"URL da API não definida. Ambiente de {api_environment}")
        if not token:
            raise ValueError(f"Token da API não definido. Ambiente de {api_environment}")
        
        # "chaveAcesso": "bda7e13e-4875-40b9-99ed-1db9fefd795e"
        # url = "https://core.fandi.com.br/v1/checkout/obter-guid"
        
        config_data = self.get_config_data(token)
        
        # "urlLogomarca": "https://revenda.com.br/logomarca.png",
        # "urlCallback": "https://revenda.com.br/checkout/callback"
        
        data = {
            "config": config_data,
            "cliente": cliente_data,
            "simulacao": {
                "quantidadeParcelas": self.env.company.installment_qty,  # Exemplo
                "valorEntrada": int(self.env.company.entry_value_percent)
            },
            "veiculo": veiculo_data,
        }
        headers = {
            "fandi-tipo-servico": "checkout",
            "Content-Type": "application/json"
        }
        guid_generator_url = "https://core.fandi.com.br/v1/checkout/obter-guid"
        guid_response = requests.post(guid_generator_url, headers=headers, data=json.dumps(data))
        guid_token = ""
        if guid_response.status_code == 200:
            guid_token = guid_response.json().get('guid')
        elif guid_response.status_code == 201:
            text = json.loads(guid_response.text)
            guid_token = text.get('retorno')
        else:
            if guid_response.content:
                result = json.loads(guid_response.content)
            elif guid_response.text:
                result = json.loads(guid_response.text)
            else:
                result = {
                    'status_code': guid_response.status_code,
                    'message': "Erro ao obter GUID"
                }
            return result
        #TODO fazer request.get apontando para a rota https://core.fandi.com.br/v1/checkout/{guid_token}
        
        guid_api_token_url = f"https://core.fandi.com.br/v1/checkout/{guid_token}"
        result = requests.get(guid_api_token_url, headers=headers)
        if result and result.status_code in [200, 201]:
            json_result = json.loads(result.content).get('retorno')
            save_guid = self.save_guid(json_result, guid_token)
            return json_result
        return None

    def simular_financiamento(self, guid, cliente_data, veiculo_data):
        # Implementação da chamada para a simulação de financiamento
        api_sim_url = f"{guid['urlFandi']}/v1/checkout/simulacao"
        headers = {
            "Authorization": f"Bearer {guid['tokenAcesso']}",
            "fandi-tipo-servico": "checkout",
            "Content-Type": "application/json",
        }
        
        guid['veiculo'].update({
            "valor": int(veiculo_data['valor'])
        })
        
        data = {
            "cliente": guid['cliente'],
            "simulacao": guid['simulacao'],
            "veiculo": guid['veiculo'],
            "institucional": {
                "empresaId": guid['empresaId'],
                "pontoVendaId": guid['pontoVendaId'],
                "cpfVendedor": guid['config']['cpfVendedor'],
            }
        }
        # valorEntrada deve ser %
        response = requests.post(api_sim_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            content = json.loads(response.content)
            if content and content.get('retorno'):
                return content.get('retorno')
        else:
            content = json.loads(response.text)
            return {
                'error': response.status_code,
                'message': content.get('message')
            }

    def create_crm_lead(self, cliente_data, veiculo_data, sim_result):
        """Cria um lead no CRM com base nos dados da simulação de financiamento."""
        self.env['crm.lead'].sudo().create({
            'name': f"Simulação de Financiamento - {cliente_data['nome']}",
            'contact_name': cliente_data['nome'],
            'partner_name': cliente_data['nome'],  # Nome do cliente
            'email_from': cliente_data['email'],  # Email do cliente
            'description': f"Financiamento do veículo {sim_result['veiculo']['fabricante']} {sim_result['veiculo']['familia']}",
            'type': 'lead',  # Pode ser 'opportunity' se for direto para oportunidade
            'vehicle_description': f"{sim_result['veiculo']['modelo']}",  # Campo customizado para descrição do veículo
            'vehicle_value': veiculo_data['valor'],  # Valor do veículo
            'installments': sim_result['quantidadeParcelas'],  # Quantidade de parcelas
            'installment_value': sim_result['valorParcela'],  # Valor da parcela
        })

    def save_guid(self, guid, guid_token):
        """Salva o GUID no banco de dados."""
        
        # fandi_client_id = self.env['fandi.webhook.client'].create({
        #     'name': guid.get('cliente', '').get('nome', ''),
        #     'cpf': guid.get('cliente', '').get('cpf', ''),
        #     'mobile_phone': guid.get('cliente', '').get('telefone', ''),
        #     'gender': guid.get('cliente', '').get('sexo', ''),
        #     'birth_date': guid.get('cliente', '').get('dataNascimento', ''),
        #     'cnh_id_card_number': guid.get('cliente', '').get('cnh', ''),
        #     'taxi_usage': guid.get('cliente', False).get('usoTaxi', False),
        #     'pcd': guid.get('cliente', False).get('pcd', False),
        #     'email': guid.get('cliente', '').get('email', ''),
        #     'company_id': self.env.company.id,
        #     'api_environment': self.env.company.api_environment
        # })
        # fandi_config_id = self.env['fandi.webhook.config'].create({
        #     'name': guid.get('config', '').get('cnpjLoja', ''),
        #     'cnpj_company': guid.get('config', '').get('cnpjLoja', ''),
        #     'cpf_seller': guid.get('config', '').get('cpfVendedor', ''),
        #     'url_logo': guid.get('config', '').get('urlLogomarca', ''),
        #     'background_color': guid.get('config', '').get('corFundo', ''),
        #     'highlight_color': guid.get('config', '').get('corDestaque', ''),
        #     'highlight_action_button': guid.get('config', '').get('corFonteBotao', ''),
        #     'url_callback': guid.get('config', '').get('urlCallback', ''),
        #     'company_id': self.env.company.id,
        #     'api_environment': self.env.company.api_environment
        # })
        self.env['fandi.webhook.call'].create({
            'name': guid_token,
            'company_id': self.env.company.id,
            'api_environment': self.env.company.api_environment,
            # 'fandi_client_id': fandi_client_id.id,
            # 'fandi_config_id': fandi_config_id.id,
            'json_body': json.dumps(guid)
        })