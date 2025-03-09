from odoo import http
from odoo.http import request
import requests
import json

class SimuladorFinanciamento(http.Controller):

    @http.route('/simulador/enviar', type='json', auth="public", website=True)
    def enviar_simulacao(self, name, cpf, telefone, product_id):
        product_id = request.env['product.template'].sudo().browse(int(product_id))
        if product_id:
            result = product_id.enviar_simulacao(name, cpf, telefone, product_id)
            return result