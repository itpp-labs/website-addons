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
    status = fields.Char(default=None)
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

    author_id = fields.Many2one('res.users', 'Author')
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
    def load_message(self, limit=20):
        self.ensure_one()
        return self.env['chess.game.chat'].message_fetch(limit=limit)

    @api.model
    def message_fetch(self, limit=20):
        return self.search(limit=limit).message_format()

    @api.multi
    def message_format(self):
        message_values = self.read([
            'id', 'date_message', 'author_id', 'game_id'
        ])
        """ for example
        {
            1: {
                date_message: 19.02.2016,
                author_id: Alex,
                game_id: 5,
                message: "hello, how are you?",
            },

            2: {
                date_message: 20.02.2016,
                author_id: Nikola,
                game_id: 5,
                message: "Hi, I'm fine",
            },
        }
        1,2, ... - it's ChatMessage.id
        """
        return message_values
