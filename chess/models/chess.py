# -*- coding: utf-8 -*-

import datetime
from openerp import models, fields, api

class ChessGame(models.Model):
    _name = 'chess.game'
    _description = 'chess game'

    game_type = fields.Selection([('blitz', 'Blitz'), ('time', 'Time'),
                                  ('free', 'Free')],'Game type')
    time_game = fields.Float(string="Game time") #If game type = time
    date_start = fields.Datetime(string='Start date') #Start game
    date_finish = fields.Datetime(string='Finish date') #Finish game
    first_user_id = fields.Many2one('res.users', 'First user', required=True)
    second_user_id = fields.Many2one('res.users', 'Second user', required=True)
    first_color_figure = fields.Selection([('white', 'White'), ('black', 'Black')],
                             'Select color for first figure')
    second_color_figure = fields.Selection([('white', 'White'), ('black', 'Black')],
                             'Select color for second figure')
    game_win = fields.Char()
    move_game_ids = fields.One2many('chess.game.line', 'game_id', 'Game Move')

class ChessGameLine(models.Model):
    _name = 'chess.game.line'
    _description = 'chess game line'

    game_id = fields.Many2one('chess.game', 'Game', required=True)
    move_game = fields.Char()
