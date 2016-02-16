# -*- coding: utf-8 -*-
from openerp import http
from openerp.addons.base import res
from openerp.http import request
import werkzeug
import datetime
import random

class Chess(http.Controller):
    @http.route('/chess/', auth="public", website=True)
    def index(self, **kw):
        users = http.request.env['res.users'].search([])
        return http.request.render('chess.chesspage', {'users': users})

    @http.route('/chess/game/<int:games>/', auth="public", website=True)
    def game(self, games):
        games_object = http.request.env['chess.game'].search([('id', '=', games)])
        if len(games_object) == 0:
            from werkzeug.exceptions import NotFound
            raise NotFound()
        return http.request.render('chess.gamepage', {'games': games_object})

    @http.route('/chess/game/', auth='public', method=['POST'], website=True)
    def create_game(self, game_type, second_user_id, first_color_figure, **kwargs):
        if second_user_id=='0':
            users = http.request.env['res.users'].search([('id', '!=', http.request.env.user.id)])
            users = [e.id for e in users]
            user_list = random.sample(users,1)
            second_user_id = user_list[0]

        if first_color_figure=='white':
            second_color_figure='black'
        else:
            second_color_figure='white'
        first_user_id = http.request.env.user.id
        new_game = http.request.env['chess.game'].create({
            'game_type': game_type,
            'date_start': datetime.datetime.now(),
            'first_user_id': first_user_id,
            'second_user_id': second_user_id,
            'first_color_figure': first_color_figure,
            'second_color_figure': second_color_figure
        })
        location = '/chess/game/'+str(new_game.id)
        return werkzeug.utils.redirect(location)

    @http.route('/chess/list/', auth='public', website=True)
    def user_list(self, **kw):
        games_completed = http.request.env['chess.game'].search([('game_win', '!=', None)])
        current_games = http.request.env['chess.game'].search([('game_win', '=', None)])
        return http.request.render('chess.listpage', {'games_completed': games_completed, 'current_games': current_games})