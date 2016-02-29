# -*- coding: utf-8 -*-

import datetime
from openerp import models, fields, api, SUPERUSER_ID

class ChessGame(models.Model):
    _name = 'chess.game'
    _description = 'chess game'

    game_type = fields.Selection([('blitz', 'Blitz'), ('limited time', 'Limited time'),
                                  ('standart', 'Standart')],'Game type')
    time_game = fields.Float(string="Game time") #If game type = limited time or blitz
    date_start = fields.Datetime(string='Start date', default=datetime.datetime.now()) #Start game
    date_finish = fields.Datetime(string='Finish date') #Finish game
    first_user_id = fields.Many2one('res.users', 'First user', required=True)
    second_user_id = fields.Many2one('res.users', 'Second user', required=True)
    first_color_figure = fields.Selection([('white', 'White'), ('black', 'Black')],
                             'Select color for first figure')
    second_color_figure = fields.Selection([('white', 'White'), ('black', 'Black')],
                             'Select color for second figure')
    game_win = fields.Char(default=None)
    move_game_ids = fields.One2many('chess.game.line', 'game_id', 'Game Move')
    message_game_ids = fields.One2many('chess.game.chat', 'game_id', 'Chat message')

class ChessGameLine(models.Model):
    _name = 'chess.game.line'
    _description = 'chess game line'

    game_id = fields.Many2one('chess.game', 'Game', required=True)
    move_game = fields.Char()

class ChatMessage(models.Model):
    _name = 'chess.game.chat'
    _description = 'chess chat message'

    game_id = fields.Many2one('chess.game','Game')
    message = fields.Char(string='Message')
    date_message = fields.Datetime(string='Date message', default = datetime.datetime.now())

    @api.one
    def broadcast(self, message):
        notifications = []

        for ps in self.env['chess.game'].search([('message_game_ids.game_id', '=', self.id)]):
            if ps.first_user_id.id != self.env.user.id:
                notifications.append([(self._cr.dbname, 'chess.game.chat', ps.first_user_id.id), message])
            else:
                notifications.append([(self._cr.dbname, 'chess.game.chat', ps.second_user_id.id), message])
        self.env['bus.bus'].sendmany(notifications)
        return 1

    @api.multi
    def load_message(self,game_id, limit=20):
        hist = self.env['chess.game.chat'].search([('game_id', '=', game_id)])
        if len(hist)>0:
            hist = [e.message for e in hist]
            return hist
        else:
            return False
