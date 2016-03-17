# -*- coding: utf-8 -*-
import openerp
from openerp import http
from openerp.http import request
from openerp.addons.base import res
import werkzeug
import datetime
import random

class Controller(openerp.addons.bus.bus.Controller):
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            channels.append((request.db, 'chess.game.chat', request.uid))
        return super(Controller, self)._poll(dbname, channels, last, options)

    #server chess chat

    @http.route('/chess/game/chat/init', type="json", auth="public")
    def init_game(self, game_id):
        author_name = http.request.env.user.name # current user
        return {'author_name': author_name, 'game_id': game_id}

    @http.route('/chess/game/chat/history', type="json", auth="public")
    def load_history(self, game_id, limit):
        history = request.env["chess.game.chat"].message_fetch(game_id, limit)
        hist = []
        for e in history:
            d = {'author_name': e.author_id.name, 'message': str(e.message), 'date_message': e.date_message}
            hist.append(d)
        history = hist
        return history

    @http.route('/chess/game/chat/send/', type="json", auth="none")
    def chat_message_send(self, game_id, message):
        res = request.env["chess.game.chat"].browse(int(game_id)).broadcast(message)
        return res

    #server chess game

    @http.route('/chess/game/move/', type="json", auth="none")
    def move_send(self, game_id, message):
        return res

    @http.route('/chess/game/load_move/', type="json", auth="none")
    def move_load(self, game_id, message):
        return res


#____________________________________________________________________________________________

class Chess(http.Controller):
    @http.route('/chess/', auth="public", website=True)
    def index(self, **kw):
        users = http.request.env['res.users'].search([('id', '!=', http.request.env.user.id)])
        return http.request.render('chess.chesspage', {'users': users})

    @http.route('/chess/game/<int:games>/', auth="public", website=True)
    def game(self, games):
        games_object = http.request.env['chess.game'].search([('id', '=', games)])
        user = http.request.env['res.users'].search([('id', '=', http.request.env.user.id)])
        if len(games_object) == 0:
            from werkzeug.exceptions import NotFound
            raise NotFound()
        return http.request.render('chess.gamepage', {'games': games_object, 'user': user})

    @http.route('/chess/game/', auth='public', website=True)
    def create_game(self, game_type=None, second_user_id=None, first_color_figure=None, **kwargs):
        if request.httprequest.method != 'POST':
            from werkzeug.exceptions import NotFound
            raise NotFound()
        if second_user_id=='0':
            users = http.request.env['res.users'].search([('id', '!=', http.request.env.user.id),('rnd_game_status', '=', True)])
            users = [e.id for e in users]
            user_list = random.sample(users,1)
            second_user_id = user_list[0]
            request.env['res.users'].message_fetch(second_user_id)

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

    #it's for examples
    # @http.route('/resultat/', auth='public', website=True)
    # def user(self, **kw):
    #     user = http.request.env['res.users'].search([('id', '!=', http.request.env.user.id),('rnd_game_status', '=', True)])
    #     print(user)
    #     print("_________________________")
    #     return http.request.render('chess.userpage', {'user': user})

    @http.route('/chess/random_game/', auth='none')
    def user_list(self, status=None, **kw):
        if status==None:
            from werkzeug.exceptions import NotFound
            raise NotFound()
        user_id = http.request.env.user.id
        request.env['res.users'].message_fetch(user_id)
        return 1
