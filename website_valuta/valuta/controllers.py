# -*- coding: utf-8 -*-
from openerp import http

class Valuta(http.Controller):
    @http.route('/etc/', auth='public', website=True)
    def index(self, **kw):
        Currencies = http.request.env['valuta.currencies']
        return http.request.render('valuta.index', {
            'currencies': Currencies.search([])
        })        
