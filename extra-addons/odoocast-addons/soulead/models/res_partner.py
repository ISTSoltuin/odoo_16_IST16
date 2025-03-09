from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    social_media_account_ids = fields.One2many(
        'social.media.account', 'partner_id', string='Social Media Accounts')