# fake_token_generator/controllers/main.py

from odoo import http

class TokenGeneratorController(http.Controller):
    @http.route('/generate_tokens', type='http', auth='user')
    def generate_tokens(self, **kwargs):
        token_generator = http.request.env['token.generator'].search([], limit=1)
        if token_generator:
            token_generator.generate_tokens()
        return "Tokens gerados com sucesso"
