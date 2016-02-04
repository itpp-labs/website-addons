# -*- coding: utf-8 -*-
from openerp import http
from openerp.addons.base import res

class Chess(http.Controller):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        users = http.request.env['res.users']
        return http.request.render('chess.homepage', {
            'users': users.search([])
        })