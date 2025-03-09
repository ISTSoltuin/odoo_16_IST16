from odoo import models, fields, api

class SocialMediaPost(models.Model):
    _name = 'social.media.post'
    _description = 'Social Media Post'

    name = fields.Char(string='Post Title', required=True)
    account_id = fields.Many2one('social.media.account', string='Social Media Account', required=True)
    content = fields.Text(string='Content', required=True)
    image = fields.Binary(string='Image')
    video = fields.Binary(string='Video')
    scheduled_date = fields.Datetime(string='Scheduled Date', required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('posted', 'Posted'),
        ('failed', 'Failed'),
    ], string='Status', default='draft')
