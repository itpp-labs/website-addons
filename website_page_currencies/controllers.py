# -*- coding: utf-8 -*-
from openerp import http
from openerp.addons.base import *

class website_page_currencies(http.Controller):
    @http.route('/etc/', auth='public', website=True)
    def index(self, **kw):
        currencies = http.request.env['res.currency']
        return http.request.render('website_page_currencies.index', {
            'currencies': currencies.search([])
        })
    
    @http.route('/currencies/<model("res.currency"):currency>/', auth='public', website=True)
    def teacher(self, currency):
        return http.request.render('website_page_currencies.biography', {
        'valuta': currency
        })    
    
    


