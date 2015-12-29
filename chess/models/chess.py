# -*- coding: utf-8 -*-

import datetime
from openerp import models, fields, api

class ChessGame(models.Model):
    _name = 'chess.game'
    _description = 'chess game'
    
    game_type = fields.Char()
    game_win = fields.Char()
    
    date_start = fields.Datetime(string='Start date') #Start game
    date_finish = fields.Datetime(string='Finish date') #Finish game
    players_ids = fields.One2many('chess.players', 'game_id', string="Players")
    
class ChessPlayers(models.Model):
    _name = 'chess.players'
    
    color_figure = fields.Char()
    user_id = fields.Many2one('res.users', 'User', required=True)
    game_id = fields.Many2one('chess.game', 'Game', required=True)
    
    
class ChessGameLine(models.Model):
    _name = 'chess.game.line'
    _description = 'chess game line'
    
    game_id = fields.Many2one('chess.game', 'Game', required=True)
    move_game = fields.Char()
    

