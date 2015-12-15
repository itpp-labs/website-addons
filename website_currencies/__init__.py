# -*- coding: utf-8 -*-
import controllers
import models
from openerp import http

class Academy(http.Controller):
    @http.route('/currencies/USD/', auth='public')
    def index(self, **kw):
        return "Hello, world"
