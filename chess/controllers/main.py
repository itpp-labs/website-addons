# -*- coding: utf-8 -*-
from openerp import http
from openerp.addons.base import res
import werkzeug

class Chess(http.Controller):
    @http.route('/chess/', auth="public", website=True)
    def index(self, **kw):
        Games = http.request.env['chess.game'].search([])
        Users = http.request.env['res.users'].search([])
        return http.request.render('chess.chesspage', {'users': Users, 'games': Games})

    @http.route('/chess/game/<int:games>/', auth="public", website=True)
    def game(self, games):
        games_object = http.request.env['chess.game'].search([('id', '=', games)])
        if len(games_object) == 0:
            from werkzeug.exceptions import NotFound
            raise NotFound()
        return http.request.render('chess.gamepage', {'games': games_object})


    @http.route('/chess/game/', auth='public', website=True)
    def redirect_index(self, **kw):
        location = '/chess'
        return werkzeug.utils.redirect(location)