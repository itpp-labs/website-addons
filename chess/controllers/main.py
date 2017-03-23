# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import werkzeug
import datetime
import random


class Chess(http.Controller):

    # chess chat
    @http.route('/chess/game/chat/init', type="json", auth="public")
    def init_chat(self, game_id):
        author_name = http.request.env.user.name  # current user
        author_id = http.request.env.user.id
        return {'author_name': author_name, 'author_id': author_id, 'game_id': game_id}

    @http.route('/chess/game/chat/history', type="json", auth="public")
    def load_history(self, game_id):
        history = request.env["chess.game.chat"].message_fetch(game_id, 100)
        if len(history) == 0:
            return False
        hist = []
        for e in history:
            d = {'author_name': str(e.author_id.name), 'message': e.message, 'date_message': e.date_message}
            hist.append(d)
        history = hist
        return history

    @http.route('/chess/game/chat/send/', type="json", auth="public")
    def chat_message_send(self, message, game_id):
        res = request.env["chess.game.chat"].broadcast(message, game_id)
        return res

    # game status
    @http.route('/chess/game/status/', type="json", auth="public")
    def game_status(self, game_id):
        result = request.env['chess.game'].create_game_status(game_id)
        return result.system_status

    # chess game
    @http.route('/chess/game/init/', type="json", auth="public")
    def init_game(self, game_id):
        result = request.env["chess.game"].browse(int(game_id)).game_information()
        return result

    @http.route('/chess/game/history', type="json", auth="public")
    def load_move(self, game_id):
        history = request.env["chess.game.line"].move_fetch(game_id)
        if len(history) == 0:
            return False
        hist = []
        for e in history:
            d = {'source': str(e.source), 'target': str(e.target)}
            hist.append(d)
        history = hist
        return history

    @http.route('/chess/game/system_history', type="json", auth="public")
    def load_system_message(self, game_id):
        history = request.env["chess.game"].system_fetch(game_id)
        if history.status == 'agreement':
            status = str(history.status)
            user = None
        else:
            if ":" in history.status:
                history = history.status.split(":")
                user = str(history[1])
                status = str(history[0])
            else:
                status = str(history[0])
                user = None
        result = {'type': 'system', 'data': {'status': str(status), 'user': str(user)}}
        return result

    @http.route('/chess/game/load_time', type='json', auth='public')
    def load_time(self, game_id, turn):
        result = request.env['chess.game'].load_time(game_id, turn)
        return result

    @http.route('/chess/game/send/', type="json", auth="public")
    def move_send(self, message, game_id):
        if message['type'] == 'move':
            result = request.env["chess.game.line"].move_broadcast(message, game_id)
            return result
        elif message['type'] == 'system':
            t = message['data']
            if t['status'] == 'time':
                result = request.env["chess.game"].system_time_broadcast(message, game_id)
            else:
                result = request.env["chess.game"].system_broadcast(message, game_id)
            return 'system'

    @http.route('/chess/game/game_over/', type="json", auth="public")
    def game_over(self, game_id, status=None, time_limit_id=None):
        request.env["chess.game"].browse(int(game_id)).game_over(status, time_limit_id)
        return True

    # create game
    @http.route('/chess/', auth="public", website=True)
    def index(self, **kw):
        users = http.request.env['res.users'].search([('id', '!=', http.request.env.user.id)])
        return http.request.render('chess.chesspage', {'users': users})

    @http.route('/chess/game/<int:games>/', auth="public", website=True)
    def game(self, games, **kwargs):
        games_object = http.request.env['chess.game'].search([('id', '=', games)])
        user = http.request.env['res.users'].search([('id', '=', http.request.env.user.id)])
        if len(games_object) == 0:
            from werkzeug.exceptions import NotFound
            raise NotFound()
        return http.request.render('chess.gamepage', {
            'games': games_object,
            'user': user,
            'dbname': request.cr.dbname,
        })

    @http.route('/chess/game/', auth='public', website=True)
    def create_game(self, game_type=None, second_user_id=None, first_color_figure=None, time_d=None, time_h=None, time_m=None, time_s=None, **kwargs):
        if request.httprequest.method != 'POST':
            from werkzeug.exceptions import NotFound
            raise NotFound()
        if second_user_id == '0':
            users = http.request.env['res.users'].search([('id', '!=', http.request.env.user.id)])
            users = [e.id for e in users]
            user_list = random.sample(users, 1)
            second_user_id = user_list[0]

        if first_color_figure == 'white':
            second_color_figure = 'black'
        else:
            second_color_figure = 'white'
        first_user_id = http.request.env.user.id
        game_time = 0
        if game_type == 'blitz' or game_type == 'limited time':
            if time_d is not None or time_h is not None or time_m is not None or time_s is not None:
                game_time = int(time_d) * 24 * 60 * 60 + int(time_h) * 60 * 60 + int(time_m) * 60 + int(time_s)
            else:
                game_time = 0
        import time
        new_game = http.request.env['chess.game'].create({
            'game_type': game_type,
            'date_start': datetime.datetime.now(),
            'first_user_id': first_user_id,
            'second_user_id': second_user_id,
            'first_color_figure': first_color_figure,
            'second_color_figure': second_color_figure,
            'second_user_time': game_time,
            'first_user_time': game_time,
            'first_time_date': float(time.time()),
            'second_time_date': float(time.time())
        })
        location = '/chess/game/' + str(new_game.id)
        return werkzeug.utils.redirect(location)

    @http.route('/chess/game/tournament', auth='public', website=True)
    def create_tournament(self, tournament_type=None, players=None, participate=None, **kwargs):
        if request.httprequest.method != 'POST':
            from werkzeug.exceptions import NotFound
            raise NotFound()
        players_clean_data = [int(x) for x in players.split(',')]
        if participate:
            players_clean_data.append(http.request.env.user.id)
        tournament = http.request.env['chess.tournament'].create({
            'tournament_type': tournament_type,
            'start_date': datetime.datetime.now(),
            'players': [(6, 0, [players_clean_data])],
            'time_d': kwargs['time_d'],
            'time_h': kwargs['time_h'],
            'time_m': kwargs['time_m'],
            'time_s': kwargs['time_s']
        })
        location = '/chess/tournament/' + str(tournament.id)
        return werkzeug.utils.redirect(location)

    @http.route('/chess/tournament/<int:tournament>/', auth="public", website=True)
    def tournament_table(self, tournament, **kwargs):
        tournament = http.request.env['chess.tournament'].search([('id', '=', tournament)])
        if len(tournament) == 0:
            from werkzeug.exceptions import NotFound
            raise NotFound()
        return http.request.render('chess.tournament-page', {
            'tournament': tournament.id,
            'uid': http.request.env.context.get('uid')
        })

    @http.route('/chess/game/tournament/fetch', type="json", auth="public")
    def fetch_tournament_data(self, tournament_id=None):
        return request.env["chess.game"].send_games_data(int(tournament_id))

    @http.route('/chess/game/tournament/create_game/', type="json", auth="public")
    def frontend_create_tournament_game(self, **kwargs):
        return request.env["chess.game"].create_tournament_game(**kwargs)
