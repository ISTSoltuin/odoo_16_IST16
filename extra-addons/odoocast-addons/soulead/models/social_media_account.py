from odoo import models, fields, api

class SocialMediaAccount(models.Model):
    _name = 'social.media.account'
    _description = 'Social Media Account'

    name = fields.Char(string='Account Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Client', required=True)
    platform = fields.Selection([
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
    ], string='Platform', required=True)
    access_token = fields.Char(string='Access Token', required=True)
    post_ids = fields.One2many('social.media.post', 'account_id', string='Posts')
