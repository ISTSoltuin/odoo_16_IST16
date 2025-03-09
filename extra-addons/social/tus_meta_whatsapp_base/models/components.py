from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class Components(models.Model):
    _name = "components"
    _description = 'Whatsapp Components'

    type = fields.Selection([('header', 'HEADER'),
                            ('body', 'BODY'),
                            ('footer', 'FOOTER'),('buttons', 'BUTTONS'),
                                           ('interactive', 'INTERACTIVE')],
                            'Type', default='header')
    formate = fields.Selection([('text', 'TEXT'),
                            ('media', 'MEDIA')],
                            'Formate', default='text')

    media_type = fields.Selection([('document', 'DOCUMENT'),
                            ('video', 'VIDEO'),
                            ('image', 'IMAGE'),],
                            'Media Type', default='document')

    text = fields.Text('Text')

    variables_ids = fields.One2many('variables','component_id','Variables')
    wa_template_id = fields.Many2one('wa.template')
    model_id = fields.Many2one('ir.model')

    button_type = fields.Selection([('none', 'None'),
                                    ('call_to_action', 'Call To Action'),
                                    ('quick_reply', 'Quick Reply')],
                                   'Button Type', default="none")
    type_of_action = fields.Selection([('PHONE_NUMBER', 'Call Phone Number'),
                                       ('URL', 'Visit Website')], 'Type of Action',
                                      default="PHONE_NUMBER")
    button_text = fields.Char(string="Button Text", size=25)
    button_text_2 = fields.Char(string="Button Text", size=25)
    button_text_3 = fields.Char(string="Button Text", size=25)
    phone_number = fields.Char(string="Phone Number", size=20)
    phone_number_2 = fields.Char(string="Phone Number", size=20)
    url_type = fields.Selection([('static', 'Static'),
                                 ('dynamic', 'Dynamic')], 'URL Type', default="static")
    url_type_2 = fields.Selection([('static', 'Static'),
                                   ('dynamic', 'Dynamic')], 'URL Type', default="static")
    name = fields.Char(string='Name', default="a")
    static_website_url = fields.Char(string="Website URL")
    static_website_url_2 = fields.Char(string="Website URL")
    dynamic_website_url = fields.Char(string='URL')
    dynamic_website_url_2 = fields.Char(string='URL')
    quick_reply_type = fields.Selection([('custom', 'Custom')], string="Type", default="custom")
    quick_reply_type_2 = fields.Selection([('custom', 'Custom')], string="Type", default="custom")
    quick_reply_type_3 = fields.Selection([('custom', 'Custom')], string="Type", default="custom")
    footer_text = fields.Char(string="Footer Text", default="Not interested? Tap Stop promotions")
    type_of_action_2 = fields.Selection([('PHONE_NUMBER', 'Call Phone Number'),
                                         ('URL', 'Visit Website')], 'Type of Action', default="URL")
    is_button_clicked = fields.Boolean(string="Is Button Clicked", default=True)
    is_second_button_clicked = fields.Boolean(string="Is Button Clicked", default=True)
    interactive_type = fields.Selection([('button', 'BUTTON'),
                                         ('list', 'LIST'),
                                         ('product', 'PRODUCT'),
                                         ('product_list', 'PRODUCT LIST')],
                                        'Interactive Message Type', default='button')
    interactive_list_ids = fields.One2many(comodel_name="interactive.list.title", inverse_name="component_id",
                                           string="List Items")
    interactive_button_ids = fields.One2many(comodel_name="interactive.button", inverse_name="component_id",
                                             string="Button Items")
    interactive_product_list_ids = fields.One2many(comodel_name="interactive.product.list", inverse_name="component_id",
                                                   string="Product List Items")
    catalog_id = fields.Char(string="Catalog ID")
    product_retailer_id = fields.Char(string="Product Retailer ID")

    def add_another_button(self):
        self.is_button_clicked = False

    def delete_button(self):
        self.is_button_clicked = True

    def delete_button_2(self):
        self.is_second_button_clicked = True

    def add_third_button(self):
        self.is_second_button_clicked = False

    @api.onchange("text")
    def onchange_text(self):
        for rec in self:
            if rec.type == 'header' and rec.formate == 'text' and rec.text and len(rec.text) > 60:
                raise UserError(_("60-character limit for headers text."))
            if rec.type == 'body' and rec.formate == 'text' and rec.text and len(rec.text) > 1024:
                raise UserError(_("1,024-character limit for body text."))

    @api.constrains('type', 'formate', 'text')
    def _constrain_text_length(self):
        for rec in self:
            if rec.type == 'header' and rec.formate == 'text' and rec.text and len(rec.text) > 60:
                raise UserError(_("60-character limit for headers text."))
            if rec.type == 'body' and rec.formate == 'text' and rec.text and len(rec.text) > 1024:
                raise UserError(_("1,024-character limit for body text."))

