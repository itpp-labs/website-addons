# -*- coding: utf-8 -*-
from openerp import http
from openerp.addons.base import res
import werkzeug
import datetime

class Chess(http.Controller):
    @http.route('/chess/', auth="public", website=True)
    def index(self, **kw):
        games = http.request.env['chess.game'].search([])
        users = http.request.env['res.users'].search([])
        return http.request.render('chess.chesspage', {'users': users, 'games': games})

    @http.route('/chess/game/<int:games>/', auth="public", website=True)
    def game(self, games):
        games_object = http.request.env['chess.game'].search([('id', '=', games)])
        if len(games_object) == 0:
            from werkzeug.exceptions import NotFound
            raise NotFound()
        return http.request.render('chess.gamepage', {'games': games_object})


    @http.route('/chess/game/', auth='public', method=['POST'], website=True)
    def create_game(self, game_type, second_user_id, first_color_figure, **kwargs):
        if first_color_figure=='white':
            second_color_figure='black'
        else:
            second_color_figure='white'
        first_user_id = http.request.env.user.id
        http.request.env['chess.game'].create({
            'game_type': game_type,
            'date_start': datetime.datetime.now(),
            'first_user_id': first_user_id,
            'second_user_id': second_user_id,
            'first_color_figure': first_color_figure,
            'second_color_figure': second_color_figure
        })

        games = http.request.env['chess.game'].search([])
        return http.request.render('chess.listpage', {'games': games})

    #def redirect_index(self, **kw):
     #   location = '/chess'
      #  return werkzeug.utils.redirect(location)

    @http.route('/chess/list/', auth='public', website=True)
    def user_list(self, **kw):
        games = http.request.env['chess.game'].search([])
        return http.request.render('chess.listpage', {'games': games})