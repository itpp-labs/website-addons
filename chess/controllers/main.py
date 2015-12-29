# -*- coding: utf-8 -*-
from openerp import http

class Chess(http.Controller):
    @http.route('/chess/', auth='public')
    def index(self, **kw):
        return http.request.render('chess.index', {
            'chess': http.request.env['chess.game'].search([])})