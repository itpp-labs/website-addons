# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Currencies(models.Model):
    _name = 'valuta.currencies'

    name = fields.Char()