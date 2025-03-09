# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Jumana Jabin MK(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
"""Franchise feedback form"""
from odoo import api, fields, models, _


class DealerSale(models.Model):
    """Franchise Dealer Monthly Sales Feedback."""
    _name = "dealer.sale"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin',
                'utm.mixin']
    _description = "Dealer Sales"
    _rec_name = "dealer_id"

    serial_no = fields.Char(string="Numero", help='Numero Licenciado', readonly=True,
                            copy=False, default='New')
    dealer_id = fields.Many2one('franchise.dealer',
                                string="Nome Licenciado",
                                help='Nome revendedor licenciado')
    franchise_reference = fields.Char(string="Referência de licenciado",
                                      readonly=True,
                                      help='Numero de Referência de licenciado')
    dealer_mail = fields.Char(string='e-mail', help='email licenciado')
    dealer_agreement_id = fields.Many2one('franchise.agreement',
                                          string="Tipo de Contrato Licenciado",
                                          help='Tipo de Contrato Licenciado')
    dealership_signed_on = fields.Date(string='licenciamento assinado',
                                       readonly=True,
                                       help='licenciamento assinado')
    sale_quantity = fields.Integer(string="Quantidade de Vendas",
                                   help='Total Quantidade de Vendas')
    scrap_quantity = fields.Integer(string="Quantidade de Perdas",
                                    help='Total de perdas')
    total_sale_amount = fields.Float(string="Valor da Venda",
                                     help='Total valor da venda')
    discount_percentage = fields.Float(string="Desconto Concedido(%)",
                                       help='Desconto Concedido(%)')
    monthly_target_amount = fields.Float(string="Meta Mensal",
                                         help='Meta Mensal valor')
    monthly_target_gained = fields.Float(string="Meta Mensal Obtida (%)",
                                         help='Meta Mensal Obtida (%)')
    state = fields.Selection(selection=[('a_to_verify', 'Verificar'),
                                        ('b_verified', 'Verificado')],
                             string='Status', required=True,
                             help='Status do registro licenciamento',
                             readonly=True, copy=False,
                             tracking=True, default='a_to_verify')

    def action_verify_sale(self):
        """Method to verify the sales feedback"""
        self.write({'state': "b_verified"})

    @api.model_create_multi
    def create(self, vals_list):
        """Method to create Franchise dealer sales record sequences."""
        for vals in vals_list:
            if vals.get('serial_no', _("New")) == _("New"):
                vals['serial_no'] = self.env['ir.sequence'].next_by_code(
                    'dealer.sale') or 'New'
            result = super(DealerSale, self).create(vals)
            return result
