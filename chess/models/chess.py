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
    first_user_id = fields.Many2one('res.users', 'First user')
    second_user_id = fields.Many2one('res.users', 'Second user')
    first_color_figure = fields.Selection([('white', 'White'), ('black', 'Black')],
                             'Select color for first figure')
    second_color_figure = fields.Selection([('white', 'White'), ('black', 'Black')],
                             'Select color for second figure')
    status = fields.Char(default=None)
    move_game_ids = fields.One2many('chess.game.line', 'game_id', 'Game Move')
    message_game_ids = fields.One2many('chess.game.chat', 'game_id', 'Chat message')

class Users(models.Model):
    _inherit = ['res.users']

    rnd_game_status = fields.Boolean(default=False)
    game_rating = fields.Float(default=0)

    @api.model
    def message_fetch(self, user_id):
        return self.search([('id', '=', user_id)]).write_status()

    @api.one
    def write_status(self):
        if self.rnd_game_status==False:
            rnd_game_status=True
            return self.write({'rnd_game_status': rnd_game_status})
        else:
            rnd_game_status=False
            return self.write({'rnd_game_status': rnd_game_status})


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
    message = fields.Text(string='Message')
    date_message = fields.Datetime(string='Date message', default = datetime.datetime.now())

    @api.one
    def broadcast(self, message):
        notifications = []

        for ps in self.env['chess.game'].search([('message_game_ids.game_id', '=', self.id)]):

            #build the new message
            author_id = self.env.user.id
            vals = {
                "author_id": author_id,
                "game_id": self.id,
                "message": message['data'],
                "date_message": datetime.datetime.now(),
            }

            # save it
            self.create(vals)

            if ps.first_user_id.id != self.env.user.id:
                notifications.append([(self._cr.dbname, 'chess.game.chat', ps.first_user_id.id), message])
            else:
                notifications.append([(self._cr.dbname, 'chess.game.chat', ps.second_user_id.id), message])
        self.env['openerp.bus.bus'].sendmany(notifications)
        return 1

    @api.model
    def message_fetch(self, game_id, limit=20):
        return self.search([('game_id', '=', game_id)], limit=limit).sorted(key=lambda r: r.id)
