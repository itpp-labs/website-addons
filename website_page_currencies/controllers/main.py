# -*- coding: utf-8 -*-
from openerp import http
from openerp.addons.base import res

class website_page_currencies(http.Controller): 
    @http.route('/currencies/<model("res.currency"):currencyline>/', auth='public', website=True)
    def index(self, currencyline, **kw):
        currencies = http.request.env['res.currency']
        return http.request.render('website_page_currencies.index', {
            'currencies': currencies.search([]), 'currencyline': currencyline
        })

    
    


