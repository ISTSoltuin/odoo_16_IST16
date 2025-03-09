# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    api_environment = fields.Selection(
    selection=[
        ('sandbox', 'Sandbox'),
        ('homologation', 'Homologação'),
        ('production', 'Produção'),
    ], string='API Environment', default='sandbox')
    
    sandbox_webhook_url = fields.Char(string='Sandbox URL')
    sandbox_token = fields.Char(string='Sandbox Token')
    
    homologation_webhook_url = fields.Char(string='Homologation URL')
    homologation_token = fields.Char(string='Homologation Token')
    
    production_webhook_url = fields.Char(string='Production URL')
    production_token = fields.Char(string='Production Token')
    
    entry_value_percent = fields.Integer(
        string="Valor Entrada (%)",
        default=0
    )
    
    installment_qty = fields.Integer(
        string="Quantidade de Parcelas",
        default=0
    )
    
    cnpj_loja = fields.Char(
        string="CNPJ Loja"
    )
    
    cpf_vendedor = fields.Char(
        string="CPF Vendedor"
    )
    
    url_logomarca = fields.Char(
        string="URL Logomarca"
    )
    
    cor_fundo = fields.Char(
        string="Cor Fundo"
    )
    
    cor_destaque = fields.Char(
        string="Cor Destaque"
    )
    
    cor_fonte_botao = fields.Char(
        string="Cor Fonte Botão"
    )
    
    url_callback = fields.Char(
        string="URL Callback"
    )