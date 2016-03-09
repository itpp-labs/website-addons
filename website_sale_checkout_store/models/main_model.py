# -*- coding: utf-8 -*-
from openerp.osv import osv, orm, fields

class sale_order(osv.Model):
    _inherit = "sale.order"
    _columns = {
        'buy_way': fields.char(),
    }