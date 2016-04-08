# -*- coding: utf-8 -*-
import datetime
import time
from openerp import models, fields, api, SUPERUSER_ID

class ChessGame(models.Model):
    _name = 'chess.game'
    _description = 'chess game'

    game_type = fields.Selection([('blitz', 'Blitz'), ('limited time', 'Limited time'),
                                  ('standart', 'Standart')],'Game type')
    first_user_time = fields.Float(string="First user time", default=0)
    first_time_date = fields.Float(default=0)
    second_user_time = fields.Float(string="Second user time", default=0)
    second_time_date = fields.Float(default=0)
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

    @api.model
    def system_time_broadcast(self, message, game_id):
        return self.search([('id', '=', game_id)]).write_time(message, game_id)

    @api.model
    def load_time(self, game_id, turn, author, color):
        return self.search([('id', '=', game_id)]).search_time(turn, author, color)

    @api.one
    def search_time(self, turn, author, color):
        author_time = self.first_user_time
        another_user_time = self.second_user_time
        author_last_time = self.first_time_date
        another_last_time = self.second_time_date
        if self.env.user.id==self.first_user_id.id:
            author_time  = self.first_user_time
            another_user_time = self.second_user_time
            author_last_time = self.first_time_date
            another_last_time = self.second_time_date
        else:
            author_time  = self.second_user_time
            another_user_time = self.first_user_time
            author_last_time = self.second_time_date
            another_last_time = self.first_time_date
        current_time = int(time.time())
        if(self.status=='Game Over'):
            return {'author_time':  author_time, 'another_user_time': another_user_time}
        else:
            if turn == 'ww' or turn == 'bb':
                result = current_time-author_last_time
                new_result = author_time-result
                if new_result < 0:
                    new_result=0
                return {'author_time':  new_result, 'another_user_time': another_user_time}
            elif turn == 'bw' or turn == 'wb':
                result = current_time-another_last_time
                new_result = another_user_time-result
                if new_result < 0:
                    new_result=0
                return {'author_time':  int(new_result), 'another_user_time': int(author_time)}

    @api.one
    def write_time(self, message, game_id):
        data = message['data']
        if self.first_user_id.name == data['user']:
            return self.write({'first_user_time': int(data['value'])})
        else:
            return self.write({'second_user_time': int(data['value'])})

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

    @api.one
    def game_over(self, status):
        #status for rating ELO
        if len(status)<=0:
            rating_first = self.first_user_id.game_rating #rating for first user
            rating_second = self.second_user_id.game_rating #rating for second use
            # #all game for first user
            all_game_f = len(self.env["chess.game"].search([('first_user_id.id', '=', self.first_user_id.id)]))\
                         +len(self.env["chess.game"].search([('second_user_id.id', '=', self.first_user_id.id)]))
            #all game for second user
            all_game_s = len(self.env["chess.game"].search([('first_user_id.id', '=', self.second_user_id.id)]))\
                         +len(self.env["chess.game"].search([('second_user_id.id', '=', self.second_user_id.id)]))
            K_f = 0
            if rating_first>2400:
                K_f = 10
            elif rating_first<2400 and all_game_f>30:
                K_f = 20
            elif all_game_f<30:
                K_f = 40

            K_s = 0
            if rating_second>2400:
                K_s = 10
            elif rating_second<2400 and all_game_s>30:
                K_s = 20
            elif all_game_s<30:
                K_s = 40
            first_game_result = 0.0
            second_game_result = 0.0
            if self.first_color_figure == status:
                first_game_result = 0.0 #he is not win
                second_game_result = 1.0 #he is win
            elif self.second_color_figure == status:
                first_game_result = 1.0 #he is win
                second_game_result = 0.0
            elif status=='drawn':
                first_game_result = 0.5
                second_game_result = 0.5
            #rating formule
            print("------------------first user-----------------")
            print('rating_first', rating_first)
            print('rating_second', rating_second)
            print('all_game_f', all_game_f)
            print('K_f', K_f)
            import math
            #new rating for first user
            E_first = (1.0/(1.0+math.pow(10,((rating_second - rating_first)/400.0))))
            new_rating_first = rating_first + K_f * (first_game_result - E_first)
            print('result game', first_game_result)
            print('result game second', second_game_result)
            print('status', status)
            print('E_first', E_first)
            print('new_rating_first', new_rating_first)
            print("---------------------------------------------")

            #new rating for second user
            E_second = (1.0/(1.0+math.pow(10,((rating_first - rating_second)/400.0))))
            new_rating_second = rating_second + K_s * (second_game_result - E_second)
            #write it
            print("_________________________________")
            print(new_rating_first)
            print(new_rating_second)
            print("_________________________________")
            self.env['res.users'].search([('id', '=', self.first_user_id.id)]).write({
                 'game_rating': new_rating_first
            })
            self.env['res.users'].search([('id', '=', self.second_user_id.id)]).write({
                 'game_rating': new_rating_second})
        return self.write({'date_finish': datetime.datetime.now(), 'status': 'Game Over'})

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

    game_rating = fields.Float(default=0.0)


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
            #if send move fist user then on time for second user
            if ps.first_user_id.id==self.env.user.id:
                ps.write({'second_time_date': int(time.time())})
            else:
                ps.write({'first_time_date': int(time.time())})
            # save it
            self.create(vals)
            ps.write({'status': 'Active game'})
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
