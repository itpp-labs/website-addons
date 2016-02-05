# -*- coding: utf-8 -*-
from openerp import http
from openerp.addons.base import res

class Chess(http.Controller):
    @http.route('/chess/', auth="public", website=True)
    def index(self, **kw):
        return http.request.render('chess.chesspage')

    @http.route('/chess/game/', auth="public", website=True)
    def game(self, **kw):
        return http.request.render('chess.gamepage')