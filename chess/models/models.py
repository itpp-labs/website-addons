# -*- coding: utf-8 -*-
import datetime
import time
from odoo import api
from odoo import fields
from odoo import models
import logging

_logger = logging.getLogger(__name__)

try:
    import chess
except (ImportError, IOError) as err:
    _logger.debug(err)


class ChessGame(models.Model):
    _name = 'chess.game'
    _description = 'chess game'

    game_type = fields.Selection([('blitz', 'Blitz'), ('limited time', 'Limited time'),
                                  ('standart', 'Standart')], 'Game type')
    first_user_time = fields.Float(string="First user time", default=0)
    first_time_date = fields.Float(default=0)
    second_user_time = fields.Float(string="Second user time", default=0)
    second_time_date = fields.Float(default=0)
    date_start = fields.Datetime(string='Start date', default=datetime.datetime.now())  # Start game
    date_finish = fields.Datetime(string='Finish date')  # Finish game
    first_user_id = fields.Many2one('res.users', 'First user')
    second_user_id = fields.Many2one('res.users', 'Second user')
    first_color_figure = fields.Selection([('white', 'White'), ('black', 'Black')],
                                          'Select color for first figure')
    second_color_figure = fields.Selection([('white', 'White'), ('black', 'Black')],
                                           'Select color for second figure')
    status = fields.Char(default='New Game')
    system_status = fields.Char(default='Waiting')
    fen = fields.Char(default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    move_game_ids = fields.One2many('chess.game.line', 'game_id', 'Game Move')
    message_game_ids = fields.One2many('chess.game.chat', 'game_id', 'Chat message')

    @api.model
    def create_game_status(self, game_id):
        return self.search([('id', '=', game_id)])

    @api.model
    def system_fetch(self, game_id):
        return self.search([('id', '=', game_id)])

    @api.model
    def system_broadcast(self, message, game_id):
        return self.search([('id', '=', game_id)]).write_game_status(message, game_id)

    @api.model
    def system_time_broadcast(self, message, game_id):
        return self.search([('id', '=', game_id)]).write_time(message, game_id)

    @api.model
    def load_time(self, game_id, turn):
        return self.search([('id', '=', game_id)]).search_time(turn)

    @api.multi
    def search_time(self, turn):
        self.ensure_one()
        if self.env.user.id == self.first_user_id.id:
            author_time = self.first_user_time
            another_user_time = self.second_user_time
            author_last_time = self.first_time_date
            another_last_time = self.second_time_date
        else:
            author_time = self.second_user_time
            another_user_time = self.first_user_time
            author_last_time = self.second_time_date
            another_last_time = self.first_time_date
        current_time = int(time.time())
        if self.system_status == 'Game Over':
            return {'author_time': author_time, 'another_user_time': another_user_time}
        else:
            if turn == 'ww' or turn == 'bb':
                result = current_time - author_last_time
                new_result = author_time - result
                if new_result < 0:
                    new_result = 0
                return {'author_time': new_result, 'another_user_time': another_user_time}
            elif turn == 'bw' or turn == 'wb':
                result = current_time - another_last_time
                new_result = another_user_time - result
                if new_result < 0:
                    new_result = 0
                return {'author_time': int(new_result), 'another_user_time': int(author_time)}

    @api.multi
    def write_time(self, message, game_id):
        data = message['data']
        if self.first_user_id.name == data['user']:
            return self.write({'first_user_time': int(data['value'])})
        else:
            return self.write({'second_user_time': int(data['value'])})

    @api.multi
    def write_game_status(self, message, game_id):
        notifications = []
        data = message['data']
        if self.first_user_id.id != self.env.user.id:
            secound_user_id = self.first_user_id.id
        else:
            secound_user_id = self.second_user_id.id

        channel = '["%s","%s",["%s","%s"]]' % (self._cr.dbname, "chess.game", secound_user_id, game_id)
        notifications.append([str(channel), message])
        self.env['bus.bus'].sendmany(notifications)
        # write it
        if len(data) == 2:
            return self.write({"status": data['status'] + ':' + data['user']})
        else:
            return self.write({"status": data['status']})

    @api.multi
    def game_over(self, status, time_limit_id):
        if self.system_status == 'Game Over':
            return False
        if time_limit_id is not False:
            if time_limit_id == self.first_user_id.id:
                self.write({'first_user_time': 0})
                first_game_result = 0
                second_game_result = 1.0
                status = self.first_color_figure
            else:
                self.write({'second_user_time': 0})
                first_game_result = 1.0
                second_game_result = 0
                status = self.second_color_figure

        # status for rating ELO
        if len(status) > 0:
            rating_first = self.first_user_id.game_rating  # rating for first user
            rating_second = self.second_user_id.game_rating  # rating for second use
            # all game for first user
            all_game_f = len(self.env["chess.game"].search([('first_user_id.id', '=', self.first_user_id.id)]))\
                + len(self.env["chess.game"].search([('second_user_id.id', '=', self.first_user_id.id)]))
            # all game for second user
            all_game_s = len(self.env["chess.game"].search([('first_user_id.id', '=', self.second_user_id.id)]))\
                + len(self.env["chess.game"].search([('second_user_id.id', '=', self.second_user_id.id)]))
            if rating_first > 2400:
                K_f = 10
            elif rating_first < 2400 and all_game_f > 30:
                K_f = 20
            elif all_game_f < 30:
                K_f = 40

            if rating_second > 2400:
                K_s = 10
            elif rating_second < 2400 and all_game_s > 30:
                K_s = 20
            elif all_game_s < 30:
                K_s = 40

            if self.first_color_figure == status:
                first_game_result = 0.0  # he is not win
                second_game_result = 1.0  # he is win
            elif self.second_color_figure == status:
                first_game_result = 1.0  # he is win
                second_game_result = 0.0
            if time_limit_id is not False:
                if time_limit_id > 0:
                    first_game_result = first_game_result
                    second_game_result = second_game_result
            # rating formule
            import math
            # new rating for first user
            E_first = (1.0 / (1.0 + math.pow(10, ((rating_second - rating_first) / 400.0))))
            new_rating_first = rating_first + K_f * (first_game_result - E_first)
            # new rating for second user
            E_second = (1.0 / (1.0 + math.pow(10, ((rating_first - rating_second) / 400.0))))
            new_rating_second = rating_second + K_s * (second_game_result - E_second)
            # write it
            self.env['res.users'].search([('id', '=', self.first_user_id.id)]).write({
                'game_rating': round(new_rating_first, 2)
            })
            self.env['res.users'].search([('id', '=', self.second_user_id.id)]).write({
                'game_rating': round(new_rating_second, 2)})

        # there is a bug in original version with lack of status in case the game were drawned
        if not status:
            first_game_result = 0.5
            second_game_result = 0.5

        return self.write(
            {
                'date_finish': datetime.datetime.now(),
                'system_status': 'Game Over',
                'first_user_score': first_game_result,
                'second_user_score': second_game_result,
            })

    @api.multi
    def accept_chess_game(self):
        vals = {
            'status': 'Active game',
            'system_status': 'Active game'
        }
        self.information_chess_game(vals)

        url = '/chess/game/%d/' % (self.id)
        return {
            'name': 'Chess game page',
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }

    @api.multi
    def refuse_chess_game(self):
        vals = {
            'status': 'Denied',
            'system_status': 'Denied'
        }
        self.information_chess_game(vals)
        return {
            'domain': "[('system_status', '=', 'Waiting'), ('first_user_id', '!=', %s)]" % (self.id),
            'name': 'Reload page',
            'view_mode': 'tree',
            'view_type': 'form',
            'res_model': 'chess.game',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def open_chess_game(self):
        url = '/chess/game/%d/' % (self.id)
        return {
            'name': 'Chess game page',
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }

    @api.multi
    def cancel_chess_game(self):
        vals = {
            'status': 'Canceled',
            'system_status': 'Canceled'
        }
        self.information_chess_game(vals)
        return {
            'domain': "[('system_status', '=', 'Waiting'), ('first_user_id', '=', %s)]" % (self.id),
            'name': 'Reload page',
            'view_mode': 'tree',
            'view_type': 'form',
            'res_model': 'chess.game',
            'type': 'ir.actions.act_window',
        }

    @api.model
    def information_chess_game(self, vals):
        self.write(vals)
        notifications = []
        if self.first_user_id.id != self.env.user.id:
            secound_user_id = self.first_user_id.id
        else:
            secound_user_id = self.second_user_id.id

        channel = '["%s","%s",["%s","%s"]]' % (self._cr.dbname, "chess.game.info", secound_user_id, self.id)
        message = {'system_status': self.status}
        notifications.append([str(channel), message])
        self.env['bus.bus'].sendmany(notifications)

    @api.multi
    def game_information(self):
        self.ensure_one()
        if self.first_user_id.id == self.env.user.id:
            author_id = self.first_user_id.id
            author_name = self.first_user_id.name
            author_color_figure = self.first_color_figure
            author_game_time = self.first_user_time

            another_user_name = self.second_user_id.name
            another_user_id = self.second_user_id.id
            another_user_color_figure = self.second_color_figure
            another_user_time = self.second_user_time
        else:
            author_id = self.second_user_id.id
            author_name = self.second_user_id.name
            author_color_figure = self.second_color_figure
            author_game_time = self.second_user_time

            another_user_name = self.first_user_id.name
            another_user_id = self.first_user_id.id
            another_user_color_figure = self.first_color_figure
            another_user_time = self.first_user_time

        data = {
            'author': {
                'name': str(author_name),
                'id': int(author_id),
                'color': str(author_color_figure),
                'time': float(author_game_time)
            },
            'information': {
                'id': self.ids[0],
                'type': str(self.game_type),
                'status': str(self.status),
                'system_status': str(self.system_status)
            },
            'another_user': {
                'name': str(another_user_name),
                'id': int(another_user_id),
                'color': str(another_user_color_figure),
                'time': float(another_user_time)
            }
        }
        return data


class Users(models.Model):
    _inherit = ['res.users']

    game_rating = fields.Float(default=1000.0)


class ChessGameLine(models.Model):
    _name = 'chess.game.line'
    _description = 'chess game line'

    game_id = fields.Many2one('chess.game', 'Game', required=True, ondelete='cascade')
    source = fields.Char()
    target = fields.Char()

    @api.model
    def move_broadcast(self, message, game_id):
        notifications = []
        for ps in self.env['chess.game'].search([('id', '=', game_id)]):
            data = message['data']
            vals = {
                "game_id": game_id,
                "source": data['source'],
                "target": data['target'],
            }
            # chess server for legal move
            board = chess.Board(ps.fen)
            legal_move = chess.Move.from_uci(data['source'] + data['target']) in board.legal_moves
            # if move not legal then maybe Queen?
            if legal_move is False:
                legal_Q = board.parse_san(data['target'] + '=Q') in board.legal_moves
                # if not Queen then fix board
                if legal_Q is False:
                    return False
            # if send move fist user then on time for second user
            if ps.first_user_id.id == self.env.user.id:
                ps.write({'second_time_date': int(time.time())})
            else:
                ps.write({'first_time_date': int(time.time())})
            ps.write({'fen': data['fen']})
            # save it
            self.create(vals)
            ps.write({'status': 'Active game', 'system_status': 'Active game'})

            if ps.first_user_id.id != self.env.user.id:
                secound_user_id = ps.first_user_id.id
            else:
                secound_user_id = ps.second_user_id.id

            channel = '["%s","%s",["%s","%s"]]' % (self._cr.dbname, "chess.game.line", secound_user_id, game_id)
            notifications.append([str(channel), message])

        self.env['bus.bus'].sendmany(notifications)
        return 'move'

    @api.model
    def move_fetch(self, game_id):
        return self.search([('game_id.id', '=', game_id)]).sorted(key=lambda r: r.id)


class ChatMessage(models.Model):
    _name = 'chess.game.chat'
    _description = 'chess chat message'

    author_id = fields.Many2one('res.users', 'Author')
    game_id = fields.Many2one('chess.game', 'Game')
    message = fields.Text(string='Message')
    date_message = fields.Datetime(string='Date message', default=datetime.datetime.now())

    @api.model
    def broadcast(self, message, game_id):
        notifications = []
        for ps in self.env['chess.game'].search([('id', '=', game_id)]):
            # build the new message
            author_id = message['author_id']
            vals = {
                "author_id": author_id,
                "game_id": game_id,
                "message": message['data'],
                "date_message": datetime.datetime.now(),
            }
            # save it
            self.create(vals)
            if ps.first_user_id.id != self.env.user.id:
                secound_user_id = ps.first_user_id.id
            else:
                secound_user_id = ps.second_user_id.id

            channel = '["%s","%s",["%s","%s"]]' % (self._cr.dbname, "chess.game.chat", secound_user_id, game_id)
            notifications.append([str(channel), message])

        self.env['bus.bus'].sendmany(notifications)
        return 1

    @api.model
    def message_fetch(self, game_id, limit=20):
        return self.search([('game_id.id', '=', game_id)], limit=limit).sorted(key=lambda r: r.id)


class Tournament(models.Model):
    _name = 'chess.tournament'

    players = fields.Many2many('res.users', string='Players')
    status = fields.Char(default='Active')
    start_date = fields.Datetime(string='Start Date', default=datetime.datetime.now())
    tournament_type = fields.Selection([('blitz', 'Blitz'), ('limited time', 'Limited time'),
                                        ('standart', 'Standart')], 'Game Type')
    games = fields.One2many('chess.game', 'tournament')
    time_d = fields.Float(default=0)
    time_h = fields.Float(default=0)
    time_m = fields.Float(default=0)
    time_s = fields.Float(default=0)

    @api.model
    def send_tournament_players_data(self, tournament_id):
        tournament = self.search([('id', '=', tournament_id)])
        players = []
        for p in tournament.players:
            players.append({'id': p.id, 'name': p.name})
        data = {
            'players': players,
            'tournament_type': tournament.tournament_type,
            'time_data': {
                'time_d': tournament.time_d,
                'time_h': tournament.time_h,
                'time_m': tournament.time_m,
                'time_s': tournament.time_s
            }
        }
        return data

    @api.model
    def send_tournament_games_data(self, tournament_id):
        tournament = self.search([('id', '=', tournament_id)])
        games = []
        for g in tournament.games:
            games.append({'id': g.id, 'player1': g.first_user_id, 'player2:': g.second_user_id})
        return games


class TournamentChessGame(models.Model):
    _inherit = ['chess.game']

    tournament = fields.Many2one('chess.tournament', ondelete='cascade')
    first_user_score = fields.Float(default=0, help='First user game result.')
    second_user_score = fields.Float(default=0, help='Second user game result.')

    @api.model
    def create_tournament_game(self, first_user_id=None, tournament_id=None, game_type=None, second_user_id=None,
                               time_d=None, time_h=None, time_m=None, time_s=None, **kwargs):
        game_time = 0
        if game_type == 'blitz' or game_type == 'limited time':
            if time_d is not None or time_h is not None or time_m is not None or time_s is not None:
                game_time = int(time_d) * 24 * 60 * 60 + int(time_h) * 60 * 60 + int(time_m) * 60 + int(time_s)
            else:
                game_time = 0
        new_game = self.env['chess.game'].create({
            'tournament': tournament_id,
            'game_type': game_type,
            'date_start': datetime.datetime.now(),
            'first_user_id': first_user_id,
            'second_user_id': second_user_id,
            'first_color_figure': 'white',
            'second_color_figure': 'black',
            'second_user_time': game_time,
            'first_user_time': game_time,
            'first_time_date': float(time.time()),
            'second_time_date': float(time.time())
        })
        return new_game.id

    @api.model
    def send_games_data(self, tournament_id):
        games = self.search([('tournament', '=', tournament_id)])
        data = []
        for game in games:
            data.append({
                'id': game.id,
                'system_status': game.system_status,
                'player1': {'id': game.first_user_id.id, 'score': game.first_user_score},
                'player2': {'id': game.second_user_id.id, 'score': game.second_user_score},
                'status': game.status,
                'date_start': game.date_start,
                'date_finish': game.date_finish,
                'tournament': game.tournament.id
            })
        return data

    @api.model
    def accept_tournament_game(self, game_id):
        return self.search([('id', '=', game_id)]).accept_chess_game()

    @api.model
    def is_tournament_game(self, game_id):
        return self.search([('id', '=', game_id)]).tournament.id
