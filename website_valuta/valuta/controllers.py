# -*- coding: utf-8 -*-
from openerp import http

# class Currencies(http.Controller):
#     @http.route('/currencies/currencies/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/currencies/currencies/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('currencies.listing', {
#             'root': '/currencies/currencies',
#             'objects': http.request.env['currencies.currencies'].search([]),
#         })

#     @http.route('/currencies/currencies/objects/<model("currencies.currencies"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('currencies.object', {
#             'object': obj
#         })