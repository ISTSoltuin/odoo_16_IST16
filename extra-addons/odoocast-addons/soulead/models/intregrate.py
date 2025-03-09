import requests
import json
from odoo import models, fields, api

class SocialMediaPost(models.Model):
    _inherit = 'social.media.post'

    @api.model
    def post_to_social_media(self):
        posts = self.search([('status', '=', 'scheduled'), ('scheduled_date', '<=', fields.Datetime.now())])
        for post in posts:
            if post.account_id.platform == 'facebook':
                url = 'https://graph.facebook.com/v12.0/me/feed'
                data = {
                    'message': post.content,
                    'access_token': post.account_id.access_token,
                }
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    post.status = 'posted'
                else:
                    post.status = 'failed'
            elif post.account_id.platform == 'instagram':
                url = 'https://graph.facebook.com/v12.0/me/media'
                data = {
                    'caption': post.content,
                    'access_token': post.account_id.access_token,
                }
                files = {}
                if post.image:
                    files['image'] = ('image.jpg', post.image.decode('base64'), 'image/jpeg')
                elif post.video:
                    files['video'] = ('video.mp4', post.video.decode('base64'), 'video/mp4')
                response = requests.post(url, data=data, files=files)
                if response.status_code == 200:
                    post.status = 'posted'
                else:
                    post.status = 'failed'
