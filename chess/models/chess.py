# -*- coding: utf-8 -*-
import datetime
from openerp import models, fields, api, SUPERUSER_ID

class ChessGame(models.Model):
    _name = 'chess.game'
    _description = 'chess game'

    game_type = fields.Selection([('blitz', 'Blitz'), ('limited time', 'Limited time'),
                                  ('standart', 'Standart')],'Game type')
    first_user_time = fields.Float(string="First user time", default=0)
    second_user_time = fields.Float(string="Second user time", default=0)
    date_start = fields.Datetime(string='Start date', default=datetime.datetime.now()) #Start game
    date_finish = fields.Datetime(string='Finish date') #Finish game
    first_user_id = fields.Many2one('res.users', 'First user')
    second_user_id = fields.Many2one('res.users', 'Second user')
    first_color_figure = fields.Selection([('white', 'White'), ('black', 'Black')],
                             'Select color for first figure')
    second_color_figure = fields.Selection([('white', 'White'), ('black', 'Black')],
                             'Select color for second figure')
    status = fields.Char(default='New Game')
    move_game_ids = fields.One2many('chess.game.line', 'game_id', 'Game Move')
    message_game_ids = fields.One2many('chess.game.chat', 'game_id', 'Chat message')

    @api.model
    def system_fetch(self, game_id):
        return self.search([('id', '=', game_id)])

    @api.model
    def system_broadcast(self, message, game_id):
        return self.search([('id', '=', game_id)]).write_game_status(message,game_id)

    @api.one
    def write_game_status(self, message, game_id):
        notifications = []
        data = message['data']
        if self.first_user_id.id != self.env.user.id:
            notifications.append([(self._cr.dbname, 'chess.game', self.first_user_id.id), message])
        else:
            notifications.append([(self._cr.dbname, 'chess.game', self.second_user_id.id), message])
        self.env['bus.bus'].sendmany(notifications)
        # write it
        return self.write({"status": data['status']+':'+data['user']})

    # @api.one
    # def game_over(self):
    #     return self.write({'date_finish': datetime.datetime.now()})

    @api.one
    def game_information(self):
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
            'author':{
                'name': str(author_name),
                'id': int(author_id),
                'color': str(author_color_figure),
                'time': float(author_game_time)
            },
            'information': {
                'id': self.ids[0],
                'type': str(self.game_type),
                'status': str(self.status)
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
            # save it
            self.create(vals)
            print(" # save it")
            if ps.first_user_id.id != self.env.user.id:
                notifications.append([(self._cr.dbname, 'chess.game.line', ps.first_user_id.id), message])
            else:
                notifications.append([(self._cr.dbname, 'chess.game.line', ps.second_user_id.id), message])
        self.env['bus.bus'].sendmany(notifications)
        return 1

    @api.model
    def move_fetch(self, game_id):
        return self.search([('game_id.id', '=', game_id)]).sorted(key=lambda r: r.id)


class ChatMessage(models.Model):
    _name = 'chess.game.chat'
    _description = 'chess chat message'

    author_id = fields.Many2one('res.users', 'Author')
    game_id = fields.Many2one('chess.game','Game')
    message = fields.Text(string='Message')
    date_message = fields.Datetime(string='Date message', default = datetime.datetime.now())

    @api.model
    def broadcast(self, message, game_id):
        notifications = []
        print('broadcast')
        for ps in self.env['chess.game'].search([('id', '=', game_id)]):
            #build the new message
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
                notifications.append([(self._cr.dbname, 'chess.game.chat', ps.first_user_id.id), message])
            else:
                notifications.append([(self._cr.dbname, 'chess.game.chat', ps.second_user_id.id), message])
        self.env['bus.bus'].sendmany(notifications)
        return 1

    @api.model
    def message_fetch(self, game_id, limit=20):
        return self.search([('game_id.id', '=', game_id)], limit=limit).sorted(key=lambda r: r.id)
