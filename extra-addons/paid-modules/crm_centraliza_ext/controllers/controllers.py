# -*- coding: utf-8 -*-
from odoo import http

# class MusicManagement(http.Controller):
#     @http.route('/music_management/music_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/music_management/music_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('music_management.listing', {
#             'root': '/music_management/music_management',
#             'objects': http.request.env['music_management.music_management'].search([]),
#         })

#     @http.route('/music_management/music_management/objects/<model("music_management.music_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('music_management.object', {
#             'object': obj
#         })