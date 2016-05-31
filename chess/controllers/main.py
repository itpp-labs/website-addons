# -*- coding: utf-8 -*-
import openerp
from openerp import http
from openerp.http import request
from openerp.addons.base import res
import werkzeug
import datetime
import random
import time

class Controller(openerp.addons.bus.bus.Controller):
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            registry, cr, uid, context = request.registry, request.cr, request.session.uid, request.context
            channels.append((request.db, 'chess.game.chat', request.uid))
            channels.append((request.db, 'chess.game.line', request.uid))
            channels.append((request.db, 'chess.game', request.uid))
        return super(Controller, self)._poll(dbname, channels, last, options)

    #server chess chat
    @http.route('/chess/game/chat/init', type="json", auth="public")
    def init_chat(self, game_id):
        author_name = http.request.env.user.name # current user
        author_id = http.request.env.user.id
        return {'author_name': author_name, 'author_id': author_id, 'game_id': game_id}

    @http.route('/chess/game/chat/history', type="json", auth="public")
    def load_history(self, game_id):
        history = request.env["chess.game.chat"].message_fetch(game_id, 100)
        if len(history)==0:
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

    #____________________________________________________________________
    #server chess game
    @http.route('/chess/game/init/', type="json", auth="public")
    def init_game(self, game_id):
        result = request.env["chess.game"].browse(int(game_id)).game_information()
        return result[0]

    @http.route('/chess/game/history', type="json", auth="public")
    def load_move(self, game_id):
        history = request.env["chess.game.line"].move_fetch(game_id)
        if len(history)==0:
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
        return result[0]

    @http.route('/chess/game/send/', type="json", auth="public")
    def move_send(self, message, game_id):
        if message['type']=='move':
            result = request.env["chess.game.line"].move_broadcast(message, game_id)
            return result
        elif message['type']=='system':
            t = message['data']
            if t['status']=='time':
                result = request.env["chess.game"].system_time_broadcast(message, game_id)
            else:
                result = request.env["chess.game"].system_broadcast(message, game_id)
            return 'system'

    @http.route('/chess/game/game_over/', type="json", auth="public")
    def game_over(self, game_id, status=None):
        request.env["chess.game"].browse(int(game_id)).game_over(status)
        return True

#____________________________________________________________________________________________

class Chess(http.Controller):
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
        return http.request.render('chess.gamepage', {'games': games_object, 'user': user})

    @http.route('/chess/game/', auth='public', website=True)
    def create_game(self, game_type=None, second_user_id=None, first_color_figure=None, time=None, **kwargs):
        if request.httprequest.method != 'POST':
            from werkzeug.exceptions import NotFound
            raise NotFound()
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
        game_time = 0
        if game_type=='blitz' or game_type=='limited time':
            if time!=None:
                game_time = time
            else:
                print("error, not time")
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
        location = '/chess/game/'+str(new_game.id)
        return werkzeug.utils.redirect(location)